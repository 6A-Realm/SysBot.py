# Title IDs
p = "010003F003A34000"
e = "0100187003A36000"
sw = "0100ABF008968000"
sh = "01008DB008C2C000"
bd = "0100000011D90000"
sp = "010018E011D92000"

# Bot Speech
getready = "Hello! Please prepare yourself, your trade is about to begin."
failed = "Failed to connect and trade with user."
success = "Here is what you traded to me:"
errormessage = "An error has occured while processing your request. Please try again."
lgpe = "SysBot.py is not made for LGPE yet."
swsh = "SysBot.py is not made for SWSH yet."

# Offsets
b1s1 = "0x4E34DD0 0xB8 0x10 0xA0 0x20 0x20 0x20"
v2b1s1 = "0x4E59E60, 0xB8, 0x10, 0xA0, 0x20, 0x20, 0x20"
LinkTradePartnerPokemonPointer = "0x4E55468, 0xB8, 0x8, 0x20"
LinkTradePartnerNamePointer = "0x4E5A930, 0xB8, 0x30, 0x108, 0x28, 0x90, 0x20, 0x0"
SceneIDPointer = "0x4E4EC50, 0xB8, 0x18 "

# Union Work - Detects states in the Union Room
UnionWorkIsGamingPointer = "0x4E4ED98, 0xB8, 0x3C" # 1 when loaded into Union Room, 0 otherwise
UnionWorkIsTalkingPointer = "0x4E4ED98, 0xB8, 0x85" # 1 when talking to another player or in box, 0 otherwise
UnionWorkPenaltyPointer = "0x4E4ED98, 0xB8, 0x9C" # 0 when no penalty, float value otherwise.