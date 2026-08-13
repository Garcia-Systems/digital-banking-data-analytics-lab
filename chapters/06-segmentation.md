# Chapter 6 — Segmentation

Segmentation means **breaking an aggregate metric into meaningful groups to see what the overall number may be hiding.** The investigation loop is overall metric → segment → compare → locate difference.

Run `python3 scripts/chapter_06_segmentation.py` to retain starts, completions, and rates by channel, device, channel + device, and source system, then drill from overall → mobile → phone → identity verification. Counts matter: 1/1 = 100% is weaker evidence than 9,500/10,000 = 95%.

Simpson's paradox is the compact warning that a changing group mix can hide or reverse within-group patterns. It is not forced into Harbor's main fixture. Segmentation locates where to investigate; it does not establish why a difference exists.
