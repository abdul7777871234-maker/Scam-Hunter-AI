from __future__ import annotations

import re
from urllib.parse import urlparse

URGENT_PATTERNS=[r"\burgent\b",r"\bimmediately\b",r"\bact now\b",r"\baction required\b",r"\blast chance\b",r"\bexpires?\b",r"\bwithin\s+\d+\s+(?:minutes?|hours?|days?)\b"]
PAYMENT_PATTERNS=[r"\bpay\b",r"\bpayment\b",r"\btransfer\b",r"\bbank transfer\b",r"\bwire transfer\b",r"\bgift card\b",r"\bbitcoin\b",r"\bcrypto(?:currency)?\b",r"\busdt\b",r"\bdeposit\b",r"\bfee\b"]
CREDENTIAL_PATTERNS=[r"\bpassword\b",r"\bpasscode\b",r"\botp\b",r"\bone[- ]time password\b",r"\bverification code\b",r"\bsecurity code\b",r"\bpin\b",r"\blogin\b",r"\busername\b"]
PERSONAL_PATTERNS=[r"\bcnic\b",r"\bpassport\b",r"\bid card\b",r"\bdate of birth\b",r"\baccount number\b",r"\bcard number\b",r"\bcredit card\b",r"\bdebit card\b"]
THREAT_PATTERNS=[r"\barrest\b",r"\bpolice\b",r"\blawsuit\b",r"\blegal action\b",r"\byou will be arrested\b",r"\baccount.{0,30}\b(?:suspend|suspended|blocked|close|closed|terminate)\b"]
REWARD_PATTERNS=[r"\bwon\b",r"\bwinner\b",r"\bprize\b",r"\breward\b",r"\blottery\b",r"\bgiveaway\b",r"\bfree money\b",r"\bcongratulations\b"]
CONTACT_PATTERNS=[r"\bwhatsapp\b",r"\btelegram\b",r"\bsignal\b",r"\bcontact me\b",r"\bmessage me\b",r"\bcall this number\b"]
URL_PATTERN=re.compile(r"(https?://[^\s<>\"]+|www\.[^\s<>\"]+)",re.I)

def _count(text,patterns):
    return sum(len(re.findall(p,text,re.I)) for p in patterns)

def _urls(text):
    return [x.rstrip(".,!?;:)]}") for x in URL_PATTERN.findall(text)]

def _url_flags(url):
    flags=[]
    candidate=url if not url.lower().startswith("www.") else "https://"+url
    try:
        p=urlparse(candidate); host=(p.hostname or "").lower()
        if not host: flags.append("URL has no recognizable hostname.")
        if any(x in host for x in ("verify","secure","account","login","support","claim","reward","wallet")):
            flags.append("Hostname contains a security/account/reward-related keyword.")
        if len(host.split("."))>4: flags.append("Unusually deep hostname.")
    except Exception:
        flags.append("URL could not be parsed normally.")
    return flags

def _flag(label,advice,severity,count=1):
    return {"label":label,"advice":advice,"severity":severity,"count":count}

def scan_text(text):
    text=str(text or "").strip()
    if not text:
        return {"level":"none","score":0,"headline":"No content was provided.","flags":[],"urls":[],"categories":[]}
    urgent=_count(text,URGENT_PATTERNS); payment=_count(text,PAYMENT_PATTERNS); credentials=_count(text,CREDENTIAL_PATTERNS)
    personal=_count(text,PERSONAL_PATTERNS); threats=_count(text,THREAT_PATTERNS); rewards=_count(text,REWARD_PATTERNS)
    contact=_count(text,CONTACT_PATTERNS); urls=_urls(text)
    flags=[]; categories=[]
    if urgent: flags.append(_flag("Urgency or pressure","Do not act immediately. Verify the request independently first.","medium",urgent)); categories.append("Urgency")
    if payment: flags.append(_flag("Money or payment request","Do not transfer money until the recipient and request are independently verified.","high",payment)); categories.append("Payment")
    if credentials: flags.append(_flag("Credential or verification request","Never share passwords, OTPs, PINs, or verification codes with an unverified contact.","high",credentials)); categories.append("Credential theft")
    if personal: flags.append(_flag("Sensitive personal information","Verify why the information is required and use an official channel.","high",personal)); categories.append("Identity information")
    if threats: flags.append(_flag("Threat or consequence language","Verify the claim through the organization's official contact information.","high",threats)); categories.append("Threat")
    if rewards: flags.append(_flag("Unexpected prize or reward","Do not pay a fee or provide sensitive information to claim an unexpected reward.","medium",rewards)); categories.append("Reward")
    if contact: flags.append(_flag("External messaging request","Verify the sender before moving the conversation to another messaging platform.","low",contact))
    url_items=[{"url":u,"flags":_url_flags(u)} for u in urls]
    if urls: flags.append(_flag("Link detected","Inspect and independently verify the destination before opening it.","medium",len(urls))); categories.append("Link")
    score=min(100,min(urgent*8,20)+min(payment*12,30)+min(credentials*18,35)+min(personal*14,25)+min(threats*16,30)+min(rewards*8,20)+min(len(urls)*8,20))
    if score>=60: level,headline="high","Multiple strong warning signals were detected."
    elif score>=25: level,headline="medium","Some warning signals were detected."
    else: level,headline=("low","A small number of warning signals were detected.") if flags else ("none","No automatic warning signals were detected.")
    return {"level":level,"score":score,"headline":headline,"flags":flags,"urls":url_items,"categories":list(dict.fromkeys(categories))}

def format_signals(scan):
    if not scan: return "No instant scan was performed."
    lines=[f"Instant heuristic scan level: {scan.get('level','none')}",f"Heuristic signal score: {scan.get('score',0)}/100",f"Summary: {scan.get('headline','')}"]
    for f in scan.get("flags",[])[:10]: lines.append(f"- {f.get('label','Signal')}: {f.get('advice','')}")
    for u in scan.get("urls",[])[:10]:
        if u.get("flags"): lines.append(f"- URL {u.get('url')}: "+"; ".join(u["flags"]))
    return "\n".join(lines)
