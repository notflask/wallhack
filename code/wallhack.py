import offsets
import pymem
import pymem.process
import keyboard

def glow():
  try:
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    print('csgo.exe - found\nclient.dll - found\nContinuing...')
    while True:
      if keyboard.is_pressed("end"):
        exit(0)

      glow_manager = pm.read_int(client + offsets.dwGlowObjectManager)
      for i in range(1, 32):
        entity = pm.read_int(client + offsets.dwEntityList + i * 0x10)

        if entity is None:
          pass

        if entity:
          entity_team_id = pm.read_int(entity + offsets.m_iTeamNum)
          entity_glow = pm.read_int(entity + offsets.m_iGlowIndex)

          if entity_team_id == 2:
            pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))
            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))

            pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)

          elif entity_team_id == 3:
            pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))
            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
              
            pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
  except:
    print('Not found process. Is csgo.exe launched?')
    input('\nPress any key to continue...')

if __name__ == '__main__':
	glow()
