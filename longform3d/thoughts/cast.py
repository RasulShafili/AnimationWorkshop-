# the cast of "What If You Could Hear Everyone's Thoughts?" — own designs, mixed skin tones, light-skinned hero
# (no near-black skin hex; no hoodies-with-drawstrings / black heads). Signature colour per character.
LOOKS = {
 "LEO":   dict(skin="f4ccb0", top="3f9a55", pants="2c3a5a", hair="c8642a", hairstyle="spiky"),
 "MIA":   dict(skin="b07850", top="8a4ab0", pants="3a3a4a", hair="1a1210", hairstyle="long", scale=0.72),
 "MOM":   dict(skin="e2b48e", top="d9a63a", pants="4a4a5a", hair="5a3a22", hairstyle="bun"),
 "DAD":   dict(skin="f0c8a8", top="4a78b8", pants="3a3f4a", hair="4a3020", hairstyle="short", glasses=True),
 "THEO":  dict(skin="7a4a2e", top="e8743b", pants="2a3448", hair="1a120c", hairstyle="curls", scale=0.98),
 "NORA":  dict(skin="e0b48c", top="2f9a8a", pants="3a3a4a", hair="2a1810", hairstyle="ponytail", headband="d9443f", scale=0.95),
 "DEX":   dict(skin="c8946a", top="2a2a30", pants="3a3a44", hair="1a120c", hairstyle="buzz", scale=1.04),
 "HALE":  dict(skin="e8c0a0", top="8a5a3a", pants="3a3a3a", hair="9a9a9a", hairstyle="bald", glasses=True),
 "PRIYA": dict(skin="a8704a", top="f0c040", pants="2a3448", hair="1a1010", hairstyle="long", scale=0.95),
}
EXTRAS = ["e8c0a0", "c8946a", "f4d0b8", "9a6a48", "e0b48c"]     # skin tones for jogger/walker/crowd
# extras (speaking/thinking ones get a cast name used by build.py: speaker id → NAME)
LOOKS.update({
 "JOGGER": dict(skin="c8946a", top="e85a7a", pants="2a2a30", hair="2a1a12", hairstyle="short"),
 "DOG":    dict(skin="f0c8a8", top="6a8a4a", pants="4a4a5a", hair="8a8a8a", hairstyle="bald", glasses=True),   # the dog walker
 "BUS":    dict(skin="e0b48c", top="e6c24a", pants="3a3f5a", hair="c8642a", hairstyle="ponytail", scale=0.95),
 "GIRL":   dict(skin="9a6a48", top="c94f7c", pants="2a3448", hair="1a1010", hairstyle="bun", scale=0.95),
 "BOY":    dict(skin="f4d0b8", top="5bc0de", pants="2c3a5a", hair="e6c24a", hairstyle="spiky", scale=0.97),
 "KID":    dict(skin="b07850", top="5cb85c", pants="3a3a4a", hair="1a1210", hairstyle="curls", scale=0.92),
 "K1":     dict(skin="e8c0a0", top="8e6fc1", pants="3a3a4a", hair="6a4a2a", hairstyle="long", scale=0.95),
 "K2":     dict(skin="c8946a", top="e8743b", pants="2a3448", hair="1a120c", hairstyle="short", scale=0.97),
 "K3":     dict(skin="f4ccb0", top="4aa39a", pants="3a3a4a", hair="e6c24a", hairstyle="ponytail", scale=0.94),
 "K4":     dict(skin="7a4a2e", top="e6c24a", pants="2a2a30", hair="1a1010", hairstyle="buzz", scale=0.98),
 "VOL":    dict(skin="e2b48e", top="f4f4f4", pants="3a4a6a", hair="4a3020", hairstyle="short"),               # c9 scanner volunteer
 "SCI":    dict(skin="a8704a", top="f4f4f4", pants="3a3a4a", hair="1a1010", hairstyle="bun", glasses=True),
})
