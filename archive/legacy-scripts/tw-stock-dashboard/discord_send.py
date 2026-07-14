#!/usr/bin/env python3
"""Send a compact trading decision/summary to a specific Discord thread.
Env: DISCORD_BOT_TOKEN
"""
import json, os, sys
import discord

def get_env():
    token = os.environ.get("DISCORD_BOT_TOKEN", "")
    channel_id = os.environ.get("DISCORD_DECISION_CHANNEL_ID") or os.environ.get("DISCORD_CHANNEL_ID", "")
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN missing")
    if not channel_id:
        raise RuntimeError("DISCORD_DECISION_CHANNEL_ID missing")
    return token, int(channel_id)

def summarise_to_embed(payload):
    # payload is a JSON string from decision.py or briefing.py
    try:
        data = json.loads(payload)
    except Exception:
        return discord.Embed(title="TW Decision", description=payload[:1900])

    if data.get("verdict"):
        verdict = data["verdict"]
        title = f"TW Decision: {data.get('ticker')} -> {verdict}"
        desc = "\n".join("- " + str(x) for x in (data.get("reasons") or []))
        embed = discord.Embed(title=title, description=desc[:4000], color=0x00AA00 if verdict == "YES" else 0xFF8800 if verdict == "HOLD" else 0xCC0000)
        if data.get("next_steps"):
            embed.add_field(name="Next steps", value="\n".join("- " + str(x) for x in data["next_steps"])[:1000], inline=False)
        if data.get("price"):
            p = data["price"]
            embed.add_field(name="Price", value=f"close={p.get('close')}, MA20={p.get('ma20')}, 52w={p.get('pct_from_52h')}%", inline=False)
        return embed

    if data.get("prices"):
        desc = "\n".join(f"{x.get('ticker')} close={x.get('close')}, rsi={x.get('rsi14')}, trend={x.get('trend')}" for x in data["prices"])
        embed = discord.Embed(title="TW Briefing", description=desc[:4000], color=0x00AAFF)
        if data.get("rules"):
            embed.add_field(name="Institutional calendar", value=json.dumps(data["rules"], ensure_ascii=False)[:1500], inline=False)
        return embed

    return discord.Embed(title="TW Output", description=json.dumps(data, ensure_ascii=False)[:4000])

async def send(payload_text: str):
    token, channel_id = get_env()
    intents = discord.Intents.default()
    async with discord.Client(intents=intents) as client:
        @client.event
        async def on_ready():
            ch = client.get_channel(channel_id)
            if ch is None:
                print(json.dumps({"ok": False, "error": "channel not found"}, ensure_ascii=False))
                await client.close()
                return
            embed = summarise_to_embed(payload_text)
            await ch.send(embed=embed)
            print(json.dumps({"ok": True, "channel_id": channel_id}, ensure_ascii=False))
            await client.close()

        await client.start(token)

def main():
    payload = sys.stdin.read()
    import asyncio
    asyncio.run(send(payload))

if __name__ == "__main__":
    main()
