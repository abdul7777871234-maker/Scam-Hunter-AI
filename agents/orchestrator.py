from __future__ import annotations

from agents.classifier import ClassifierAgent
from agents.rag_agent import RAGAgent
from agents.web_agent import WebResearchAgent
from agents.evidence_agent import EvidenceAgent
from agents.pattern_agent import ScamPatternAgent
from agents.contradiction_agent import ContradictionAgent
from agents.critic_agent import CriticAgent
from agents.judge_agent import JudgeAgent
from agents.response_agent import ResponseAgent


class InvestigationOrchestrator:
    """Coordinates the complete ScamHunter AI investigation pipeline."""

    def __init__(self, router, retriever, web_search, settings):
        self.router = router
        self.settings = settings

        self.classifier = ClassifierAgent(router)
        self.rag = RAGAgent(retriever, settings)
        self.web = WebResearchAgent(web_search)
        self.evidence = EvidenceAgent(router)
        self.pattern = ScamPatternAgent(router)
        self.contradiction = ContradictionAgent(router)
        self.critic = CriticAgent(router)
        self.judge = JudgeAgent(router)
        self.response = ResponseAgent(router)

    def run(self, user_text: str) -> dict:
        events = []

        # 1. Classify the investigation request
        classification = self.classifier.run(user_text)
        events.append("Input classified")

        # 2. Search the internal knowledge base
        if classification.get("requires_rag", True):
            rag = self.rag.run(user_text)
        else:
            rag = {
                "items": [],
                "evidence": [],
            }

        events.append("Knowledge base searched")

        # 3. Perform web research when required
        web = {
            "items": [],
            "cached": False,
        }

        if classification.get("requires_web", False):
            web = self.web.run(user_text[:2500])
            events.append("Web research completed")

        # 4. Analyze all available evidence
        evidence = self.evidence.run(
            user_text,
            rag,
            web,
        )
        events.append("Evidence analyzed")

        # 5. Identify possible scam patterns
        pattern = self.pattern.run(
            user_text,
            evidence["analysis"],
        )
        events.append("Scam patterns analyzed")

        # 6. Check evidence for contradictions
        contradiction = self.contradiction.run(
            evidence["evidence"],
        )
        events.append("Contradictions checked")

        # 7. Review evidence and produce an assessment
        judge = self.judge.run(
            pattern,
            contradiction,
            evidence["evidence"],
        )
        events.append("Evidence reviewed")

        # 8. Generate the first response draft
        draft = self.response.run(
            user_text,
            pattern,
            contradiction,
            judge,
            evidence["evidence"],
        )
        events.append("Response synthesized")

        # 9. Perform final quality and safety review
        critique = self.critic.run(
            draft,
            evidence["evidence"],
        )
        events.append("Final quality check completed")

        # 10. Generate the final response using the quality review
        final = self.response.run(
            user_text,
            pattern + "\n\nQUALITY CHECK:\n" + critique,
            contradiction,
            judge,
            evidence["evidence"],
        )

        return {
            "answer": final,
            "classification": classification,
            "events": events,
            "rag": rag,
            "web": web,
            "pattern": pattern,
            "contradiction": contradiction,
            "judge": judge,
            "critique": critique,
        }
