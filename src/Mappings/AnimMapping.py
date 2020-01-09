import logging

from src.DataClasses.Anims.Mappings import Entry
from src.Helpers.logger import *


class AnimSetMapping(object):

    def __init__(self, setType):
        self.map = []
        self.tempSet = []

        if setType == "anim":
            self.__GetAnimMapping()
        elif setType == "sample":
            self.__GetSampleMapping()
        else:
            logging.warning(warning("Unknown anim set type! (" + setType + ")"))

    def __GetAnimMapping(self):
        # Valid for 1.24
        self.__Add("Unknown", "flame_blue")
        self.__Add("Common", "Bomb")
        self.__Add("Common", "smoke_poof")
        self.__Add("Common", "explosion_rf")
        self.__Add("Common", "explosion_small")
        self.__Add("Common", "explosion_large")
        self.__Add("Common", "smoke_circling_gray")
        self.__Add("Common", "smoke_circling_brown")
        self.__Add("Unknown", "bubble")
        self.__Add("Unknown", "brown_thing")
        self.__Add("Common", "explosion_pepper")
        self.__Add("Unknown", "bullet_maybe_electro")
        self.__Add("Weapon", "bullet_maybe_electro")
        self.__Add("Unknown", "bullet_maybe_electro_trail")
        self.__Add("Weapon", "bullet_maybe_electro_trail")
        self.__Add("Unknown", "flame_red")
        self.__Add("Weapon", "bullet_shield_fireball")
        self.__Add("Unknown", "flare_diag_downleft")
        self.__Add("Unknown", "flare_hor")
        self.__Add("Weapon", "bullet_blaster")
        self.__Add("UI", "blaster_upgraded_jazz")
        self.__Add("UI", "blaster_upgraded_spaz")
        self.__Add("Weapon", "bullet_blaster_upgraded")
        self.__Add("Weapon", "bullet_blaster_upgraded_ver")
        self.__Add("Weapon", "bullet_blaster_ver")
        self.__Add("Weapon", "bullet_bouncer")
        self.__Add("Pickup", "ammo_bouncer_upgraded")
        self.__Add("Pickup", "ammo_bouncer")
        self.__Add("Weapon", "bullet_bouncer_upgraded")
        self.__Add("Weapon", "bullet_freezer_hor")
        self.__Add("Pickup", "ammo_freezer_upgraded")
        self.__Add("Pickup", "ammo_freezer")
        self.__Add("Weapon", "bullet_freezer_upgraded_hor")
        self.__Add("Weapon", "bullet_freezer_ver")
        self.__Add("Weapon", "bullet_freezer_upgraded_ver")
        self.__Add("Pickup", "ammo_seeker_upgraded")
        self.__Add("Pickup", "ammo_seeker")
        self.__Add("Weapon", "bullet_seeker_ver_down")
        self.__Add("Weapon", "bullet_seeker_diag_downright")
        self.__Add("Weapon", "bullet_seeker_hor")
        self.__Add("Weapon", "bullet_seeker_ver_up")
        self.__Add("Weapon", "bullet_seeker_diag_upright")
        self.__Add("Weapon", "bullet_seeker_upgraded_ver_down")
        self.__Add("Weapon", "bullet_seeker_upgraded_diag_downright")
        self.__Add("Weapon", "bullet_seeker_upgraded_hor")
        self.__Add("Weapon", "bullet_seeker_upgraded_ver_up")
        self.__Add("Weapon", "bullet_seeker_upgraded_diag_upright")
        self.__Add("Weapon", "bullet_rf_hor")
        self.__Add("Weapon", "bullet_rf_diag_downright")
        self.__Add("Weapon", "bullet_rf_upgraded_diag_downright")
        self.__Add("Pickup", "ammo_rf_upgraded")
        self.__Add("Pickup", "ammo_rf")
        self.__Add("Weapon", "bullet_rf_upgraded_hor")
        self.__Add("Weapon", "bullet_rf_upgraded_ver")
        self.__Add("Weapon", "bullet_rf_upgraded_diag_upright")
        self.__Add("Weapon", "bullet_rf_ver")
        self.__Add("Weapon", "bullet_rf_diag_upright")
        self.__Add("Weapon", "bullet_toaster")
        self.__Add("Pickup", "ammo_toaster_upgraded")
        self.__Add("Pickup", "ammo_toaster")
        self.__Add("Weapon", "bullet_toaster_upgraded")
        self.__Add("Weapon", "bullet_tnt")
        self.__Add("Weapon", "bullet_fireball_hor")
        self.__Add("Pickup", "ammo_pepper_upgraded")
        self.__Add("Pickup", "ammo_pepper")
        self.__Add("Weapon", "bullet_fireball_upgraded_hor")
        self.__Add("Weapon", "bullet_fireball_ver")
        self.__Add("Weapon", "bullet_fireball_upgraded_ver")
        self.__Add("Weapon", "bullet_bladegun")
        self.__Add("Pickup", "ammo_electro_upgraded")
        self.__Add("Pickup", "ammo_electro")
        self.__Add("Weapon", "bullet_bladegun_upgraded")
        self.__Add("Common", "explosion_tiny")
        self.__Add("Common", "explosion_freezer_maybe")
        self.__Add("Common", "explosion_tiny_black")
        self.__Add("Weapon", "bullet_fireball_upgraded_hor_2")
        self.__Add("Unknown", "flare_hor_2")
        self.__Add("Unknown", "green_explosion")
        self.__Add("Weapon", "bullet_bladegun_alt")
        self.__Add("Weapon", "bullet_tnt_explosion")
        self.__Add("Object", "container_ammo_shrapnel_1")
        self.__Add("Object", "container_ammo_shrapnel_2")
        self.__Add("Common", "explosion_upwards")
        self.__Add("Common", "explosion_bomb")
        self.__Add("Common", "smoke_circling_white")
        self.__NextSet()
        self.__Add("Bat", "idle")
        self.__Add("Bat", "resting")
        self.__Add("Bat", "takeoff_1")
        self.__Add("Bat", "takeoff_2")
        self.__Add("Bat", "roost")
        self.__NextSet()
        self.__Add("Bee", "swarm")
        self.__NextSet()
        self.__Add("Bee", "swarm_2")
        self.__NextSet()
        self.__Add("Object", "PushBoxCrate")
        self.__NextSet()
        self.__Add("Object", "PushBoxRock")
        self.__NextSet()
        self.__Add("Unknown", "diamondus_tileset_tree")
        self.__NextSet()
        self.__Add("Bilsy", "throw_fireball")
        self.__Add("Bilsy", "appear")
        self.__Add("Bilsy", "vanish")
        self.__Add("Bilsy", "bullet_fireball")
        self.__Add("Bilsy", "idle")
        self.__NextSet()
        self.__Add("Birdy", "charge_diag_downright")
        self.__Add("Birdy", "charge_ver")
        self.__Add("Birdy", "charge_diag_upright")
        self.__Add("Birdy", "caged")
        self.__Add("Birdy", "cage_destroyed")
        self.__Add("Birdy", "die")
        self.__Add("Birdy", "feather_green")
        self.__Add("Birdy", "feather_red")
        self.__Add("Birdy", "feather_green_and_red")
        self.__Add("Birdy", "fly")
        self.__Add("Birdy", "hurt")
        self.__Add("Birdy", "idle_worm")
        self.__Add("Birdy", "idle_turn_head_left")
        self.__Add("Birdy", "idle_look_left")
        self.__Add("Birdy", "idle_turn_head_left_back")
        self.__Add("Birdy", "idle_turn_head_right")
        self.__Add("Birdy", "idle_look_right")
        self.__Add("Birdy", "idle_turn_head_right_back")
        self.__Add("Birdy", "idle")
        self.__Add("Birdy", "corpse")
        self.__NextSet()
        self.__Add("Unimplemented", "BonusBirdy")
        self.__NextSet()
        self.__Add("Platform", "ball")
        self.__Add("Platform", "ball_chain")
        self.__NextSet()
        self.__Add("Object", "BonusActive")
        self.__Add("Object", "BonusInactive")
        self.__NextSet()
        self.__Add("UI", "boss_health_bar", skipNormalMap=True)
        self.__NextSet()
        self.__Add("Bridge", "Rope")
        self.__Add("Bridge", "Stone")
        self.__Add("Bridge", "Vine")
        self.__Add("Bridge", "StoneRed")
        self.__Add("Bridge", "Log")
        self.__Add("Bridge", "Gem")
        self.__Add("Bridge", "Lab")
        self.__NextSet()
        self.__Add("Bubba", "spew_fireball")
        self.__Add("Bubba", "corpse")
        self.__Add("Bubba", "jump")
        self.__Add("Bubba", "jump_fall")
        self.__Add("Bubba", "fireball")
        self.__Add("Bubba", "hop")
        self.__Add("Bubba", "tornado")
        self.__Add("Bubba", "tornado_start")
        self.__Add("Bubba", "tornado_end")
        self.__NextSet()
        self.__Add("Bee", "Bee")
        self.__Add("Bee", "bee_turn")
        self.__NextSet()
        self.__Add("Unimplemented", "butterfly")
        self.__NextSet()
        self.__Add("Pole", "Carrotus")
        self.__NextSet()
        self.__Add("Cheshire", "platform_appear")
        self.__Add("Cheshire", "platform_vanish")
        self.__Add("Cheshire", "platform_idle")
        self.__Add("Cheshire", "platform_invisible")
        self.__NextSet()
        self.__Add("Cheshire", "hook_appear")
        self.__Add("Cheshire", "hook_vanish")
        self.__Add("Cheshire", "hook_idle")
        self.__Add("Cheshire", "hook_invisible")
        self.__NextSet()
        self.__Add("Caterpillar", "exhale_start")
        self.__Add("Caterpillar", "exhale")
        self.__Add("Caterpillar", "disoriented")
        self.__Add("Caterpillar", "idle")
        self.__Add("Caterpillar", "inhale_start")
        self.__Add("Caterpillar", "inhale")
        self.__Add("Caterpillar", "smoke")
        self.__NextSet()
        self.__Add("BirdyYellow", "charge_diag_downright_placeholder")
        self.__Add("BirdyYellow", "charge_ver")
        self.__Add("BirdyYellow", "charge_diag_upright")
        self.__Add("BirdyYellow", "caged")
        self.__Add("BirdyYellow", "cage_destroyed")
        self.__Add("BirdyYellow", "die")
        self.__Add("BirdyYellow", "feather_blue")
        self.__Add("BirdyYellow", "feather_yellow")
        self.__Add("BirdyYellow", "feather_blue_and_yellow")
        self.__Add("BirdyYellow", "fly")
        self.__Add("BirdyYellow", "hurt")
        self.__Add("BirdyYellow", "idle_worm")
        self.__Add("BirdyYellow", "idle_turn_head_left")
        self.__Add("BirdyYellow", "idle_look_left")
        self.__Add("BirdyYellow", "idle_turn_head_left_back")
        self.__Add("BirdyYellow", "idle_turn_head_right")
        self.__Add("BirdyYellow", "idle_look_right")
        self.__Add("BirdyYellow", "idle_turn_head_right_back")
        self.__Add("BirdyYellow", "idle")
        self.__Add("BirdyYellow", "corpse")
        self.__NextSet()
        self.__Add("Common", "water_bubble_1")
        self.__Add("Common", "water_bubble_2")
        self.__Add("Common", "water_bubble_3")
        self.__Add("Common", "water_splash")
        self.__NextSet()
        self.__Add("Jazz", "gameover_continue")
        self.__Add("Jazz", "gameover_idle")
        self.__Add("Jazz", "gameover_end")
        self.__Add("Spaz", "gameover_continue")
        self.__Add("Spaz", "gameover_idle")
        self.__Add("Spaz", "gameover_end")
        self.__NextSet()
        self.__Add("Demon", "idle")
        self.__Add("Demon", "attack_start")
        self.__Add("Demon", "attack")
        self.__Add("Demon", "attack_end")
        self.__NextSet()  # Green rectangles (?)
        self.__Add("Unknown", "green_rectangle1")
        self.__Add("Unknown", "green_rectangle2")
        self.__Add("Unknown", "green_rectangle3")
        self.__Add("Unknown", "green_rectangle4")
        self.__Add("Common", "IceBlock")
        self.__NextSet()
        self.__Add("Devan", "bullet_small")
        self.__Add("Devan", "remote_idle")
        self.__Add("Devan", "remote_fall_warp_out")
        self.__Add("Devan", "remote_fall")
        self.__Add("Devan", "remote_fall_rotate")
        self.__Add("Devan", "remote_fall_warp_in")
        self.__Add("Devan", "remote_warp_out")
        self.__NextSet()
        self.__Add("Devan", "demon_spew_fireball")
        self.__Add("Devan", "disoriented")
        self.__Add("Devan", "freefall")
        self.__Add("Devan", "disoriented_start")
        self.__Add("Devan", "demon_fireball")
        self.__Add("Devan", "demon_fly")
        self.__Add("Devan", "demon_transform_start")
        self.__Add("Devan", "demon_transform_end")
        self.__Add("Devan", "disarmed_idle")
        self.__Add("Devan", "demon_turn")
        self.__Add("Devan", "disarmed_warp_in")
        self.__Add("Devan", "disoriented_warp_out")
        self.__Add("Devan", "disarmed")
        self.__Add("Devan", "crouch")
        self.__Add("Devan", "shoot")
        self.__Add("Devan", "disarmed_gun")
        self.__Add("Devan", "jump")
        self.__Add("Devan", "bullet")
        self.__Add("Devan", "run")
        self.__Add("Devan", "run_end")
        self.__Add("Devan", "jump_end")
        self.__Add("Devan", "idle")
        self.__Add("Devan", "warp_in")
        self.__Add("Devan", "warp_out")
        self.__NextSet()
        self.__Add("Pole", "Diamondus")
        self.__NextSet()
        self.__Add("Doggy", "attack")
        self.__Add("Doggy", "walk")
        self.__NextSet()
        self.__Add("Unimplemented", "door")
        self.__Add("Unimplemented", "door_enter_jazz_spaz")
        self.__NextSet()
        self.__Add("Dragonfly", "idle")
        self.__NextSet()
        self.__Add("Dragon", "attack")
        self.__Add("Dragon", "idle")
        self.__Add("Dragon", "turn")
        self.__NextSet()
        self.__NextSet()
        self.__NextSet()
        self.__NextSet()
        self.__NextSet()
        self.__NextSet()
        self.__Add("Eva", "Blink")
        self.__Add("Eva", "Idle")
        self.__Add("Eva", "KissStart")
        self.__Add("Eva", "KissEnd")
        self.__NextSet()
        self.__Add("UI", "icon_birdy")
        self.__Add("UI", "icon_birdy_yellow")
        self.__Add("UI", "icon_frog")
        self.__Add("UI", "icon_jazz")
        self.__Add("UI", "icon_lori")
        self.__Add("UI", "icon_spaz")
        self.__NextSet()
        self.__NextSet()
        self.__Add("FatChick", "attack")
        self.__Add("FatChick", "walk")
        self.__NextSet()
        self.__Add("Fencer", "attack")
        self.__Add("Fencer", "idle")
        self.__NextSet()
        self.__Add("Fish", "attack")
        self.__Add("Fish", "idle")
        self.__NextSet()
        self.__Add("CTF", "arrow")
        self.__Add("CTF", "base")
        self.__Add("CTF", "lights")
        self.__Add("CTF", "flag_blue")
        self.__Add("UI", "ctf_flag_blue")
        self.__Add("CTF", "base_eva")
        self.__Add("CTF", "base_eva_cheer")
        self.__Add("CTF", "flag_red")
        self.__Add("UI", "ctf_flag_red")
        self.__NextSet()
        self.__Add("Unknown", "strange_green_circles")
        self.__NextSet()
        self.__Add("UI", "font_medium")
        self.__Add("UI", "font_small")
        self.__Add("UI", "font_large")
        self.__Add("UI", "logo", skipNormalMap=True)
        self.__NextSet()
        self.__Add("Frog", "fall_land")
        self.__Add("Frog", "hurt")
        self.__Add("Frog", "idle")
        self.__Add("Jazz", "transform_frog")
        self.__Add("Frog", "fall")
        self.__Add("Frog", "jump_start")
        self.__Add("Frog", "crouch")
        self.__Add("Lori", "transform_frog")
        self.__Add("Frog", "tongue_diag_upright")
        self.__Add("Frog", "tongue_hor")
        self.__Add("Frog", "tongue_ver")
        self.__Add("Spaz", "transform_frog")
        self.__Add("Frog", "run")
        self.__NextSet()
        self.__Add("Platform", "carrotus_fruit")
        self.__Add("Platform", "carrotus_fruit_chain")
        self.__NextSet()
        self.__Add("Pickup", "gem_gemring")
        self.__NextSet()
        self.__Add("Unimplemented", "boxing_glove_stiff")
        self.__Add("Unimplemented", "boxing_glove_stiff_idle")
        self.__Add("Unimplemented", "boxing_glove_normal")
        self.__Add("Unimplemented", "boxing_glove_normal_idle")
        self.__Add("Unimplemented", "boxing_glove_relaxed")
        self.__Add("Unimplemented", "boxing_glove_relaxed_idle")
        self.__NextSet()
        self.__Add("Platform", "carrotus_grass")
        self.__Add("Platform", "carrotus_grass_chain")
        self.__NextSet()
        self.__Add("MadderHatter", "cup")
        self.__Add("MadderHatter", "hat")
        self.__Add("MadderHatter", "attack")
        self.__Add("MadderHatter", "bullet_spit")
        self.__Add("MadderHatter", "walk")
        self.__NextSet()
        self.__Add("Helmut", "idle")
        self.__Add("Helmut", "walk")
        self.__NextSet()
        self.__NextSet()
        self.__Add("Jazz", "airboard")
        self.__Add("Jazz", "airboard_turn")
        self.__Add("Jazz", "buttstomp_end")
        self.__Add("Jazz", "corpse")
        self.__Add("Jazz", "die")
        self.__Add("Jazz", "crouch_start")
        self.__Add("Jazz", "crouch")
        self.__Add("Jazz", "crouch_shoot")
        self.__Add("Jazz", "crouch_end")
        self.__Add("Jazz", "vine_walk")
        self.__Add("Jazz", "eol")
        self.__Add("Jazz", "fall")
        self.__Add("Jazz", "buttstomp")
        self.__Add("Jazz", "fall_end")
        self.__Add("Jazz", "shoot")
        self.__Add("Jazz", "shoot_ver")
        self.__Add("Jazz", "shoot_end")
        self.__Add("Jazz", "transform_frog_end")
        self.__Add("Jazz", "vine_shoot_start")
        self.__Add("Jazz", "vine_shoot_up_end")
        self.__Add("Jazz", "vine_shoot_up")
        self.__Add("Jazz", "vine_idle")
        self.__Add("Jazz", "vine_idle_flavor")
        self.__Add("Jazz", "vine_shoot_end")
        self.__Add("Jazz", "vine_shoot")
        self.__Add("Jazz", "copter")
        self.__Add("Jazz", "copter_shoot_start")
        self.__Add("Jazz", "copter_shoot")
        self.__Add("Jazz", "pole_h")
        self.__Add("Jazz", "hurt")
        self.__Add("Jazz", "idle_flavor_1")
        self.__Add("Jazz", "idle_flavor_2")
        self.__Add("Jazz", "idle_flavor_3")
        self.__Add("Jazz", "idle_flavor_4")
        self.__Add("Jazz", "idle_flavor_5")
        self.__Add("Jazz", "vine_shoot_up_start")
        self.__Add("Jazz", "fall_shoot")
        self.__Add("Jazz", "jump_unknown_1")
        self.__Add("Jazz", "jump_unknown_2")
        self.__Add("Jazz", "jump")
        self.__Add("Jazz", "ledge")
        self.__Add("Jazz", "lift")
        self.__Add("Jazz", "lift_jump_light")
        self.__Add("Jazz", "lift_jump_heavy")
        self.__Add("Jazz", "lookup_start")
        self.__Add("Jazz", "dizzy_walk")
        self.__Add("Jazz", "push")
        self.__Add("Jazz", "shoot_start")
        self.__Add("Jazz", "revup_start")
        self.__Add("Jazz", "revup")
        self.__Add("Jazz", "revup_end")
        self.__Add("Jazz", "fall_diag")
        self.__Add("Jazz", "jump_diag")
        self.__Add("Jazz", "ball")
        self.__Add("Jazz", "run")
        self.__Add("Jazz", "dash_start")
        self.__Add("Jazz", "dash")
        self.__Add("Jazz", "dash_stop")
        self.__Add("Jazz", "walk_stop")
        self.__Add("Jazz", "run_stop")
        self.__Add("Jazz", "Spring")
        self.__Add("Jazz", "idle")
        self.__Add("Jazz", "uppercut")
        self.__Add("Jazz", "uppercut_end")
        self.__Add("Jazz", "uppercut_start")
        self.__Add("Jazz", "dizzy")
        self.__Add("Jazz", "swim_diag_downright")
        self.__Add("Jazz", "swim_right")
        self.__Add("Jazz", "swim_diag_right_to_downright")
        self.__Add("Jazz", "swim_diag_right_to_upright")
        self.__Add("Jazz", "swim_diag_upright")
        self.__Add("Jazz", "swing")
        self.__Add("Jazz", "warp_in")
        self.__Add("Jazz", "warp_out_freefall")
        self.__Add("Jazz", "freefall")
        self.__Add("Jazz", "warp_in_freefall")
        self.__Add("Jazz", "warp_out")
        self.__Add("Jazz", "pole_v")
        self.__NextSet()
        self.__Add("Unimplemented", "bonus_jazz_idle_flavor")
        self.__Add("Unimplemented", "bonus_jazz_jump")
        self.__Add("Unimplemented", "bonus_jazz_ball")
        self.__Add("Unimplemented", "bonus_jazz_run")
        self.__Add("Unimplemented", "bonus_jazz_dash")
        self.__Add("Unimplemented", "bonus_jazz_rotate")
        self.__Add("Unimplemented", "bonus_jazz_idle")
        self.__NextSet()
        self.__NextSet()
        self.__Add("Pole", "Jungle")
        self.__NextSet()
        self.__Add("LabRat", "attack")
        self.__Add("LabRat", "idle")
        self.__Add("LabRat", "walk")
        self.__NextSet()
        self.__Add("Lizard", "copter_attack")
        self.__Add("Lizard", "bomb")
        self.__Add("Lizard", "copter_idle")
        self.__Add("Lizard", "copter")
        self.__Add("Lizard", "walk")
        self.__NextSet()
        self.__Add("Lori", "airboard")
        self.__Add("Lori", "airboard_turn")
        self.__Add("Lori", "buttstomp_end")
        self.__Add("Lori", "corpse")
        self.__Add("Lori", "die")
        self.__Add("Lori", "crouch_start")
        self.__Add("Lori", "crouch")
        self.__Add("Lori", "crouch_shoot")
        self.__Add("Lori", "crouch_end")
        self.__Add("Lori", "vine_walk")
        self.__Add("Lori", "eol")
        self.__Add("Lori", "fall")
        self.__Add("Lori", "buttstomp")
        self.__Add("Lori", "fall_end")
        self.__Add("Lori", "shoot")
        self.__Add("Lori", "shoot_ver")
        self.__Add("Lori", "shoot_end")
        self.__Add("Lori", "transform_frog_end")
        self.__Add("Lori", "vine_shoot_start")
        self.__Add("Lori", "vine_shoot_up_end")
        self.__Add("Lori", "vine_shoot_up")
        self.__Add("Lori", "vine_idle")
        self.__Add("Lori", "vine_idle_flavor")
        self.__Add("Lori", "vine_shoot_end")
        self.__Add("Lori", "vine_shoot")
        self.__Add("Lori", "copter")
        self.__Add("Lori", "copter_shoot_start")
        self.__Add("Lori", "copter_shoot")
        self.__Add("Lori", "pole_h")
        self.__Add("Lori", "hurt")
        self.__Add("Lori", "idle_flavor_1")
        self.__Add("Lori", "idle_flavor_2")
        self.__Add("Lori", "idle_flavor_3")
        self.__Add("Lori", "idle_flavor_4")
        self.__Add("Lori", "idle_flavor_5")
        self.__Add("Lori", "vine_shoot_up_start")
        self.__Add("Lori", "fall_shoot")
        self.__Add("Lori", "jump_unknown_1")
        self.__Add("Lori", "jump_unknown_2")
        self.__Add("Lori", "jump")
        self.__Add("Lori", "ledge")
        self.__Add("Lori", "lift")
        self.__Add("Lori", "lift_jump_light")
        self.__Add("Lori", "lift_jump_heavy")
        self.__Add("Lori", "lookup_start")
        self.__Add("Lori", "dizzy_walk")
        self.__Add("Lori", "push")
        self.__Add("Lori", "shoot_start")
        self.__Add("Lori", "revup_start")
        self.__Add("Lori", "revup")
        self.__Add("Lori", "revup_end")
        self.__Add("Lori", "fall_diag")
        self.__Add("Lori", "jump_diag")
        self.__Add("Lori", "ball")
        self.__Add("Lori", "run")
        self.__Add("Lori", "dash_start")
        self.__Add("Lori", "dash")
        self.__Add("Lori", "dash_stop")
        self.__Add("Lori", "walk_stop")
        self.__Add("Lori", "run_stop")
        self.__Add("Lori", "Spring")
        self.__Add("Lori", "idle")
        self.__Add("Lori", "uppercut_placeholder_1")
        self.__Add("Lori", "uppercut_placeholder_2")
        self.__Add("Lori", "sidekick")
        self.__Add("Lori", "dizzy")
        self.__Add("Lori", "swim_diag_downright")
        self.__Add("Lori", "swim_right")
        self.__Add("Lori", "swim_diag_right_to_downright")
        self.__Add("Lori", "swim_diag_right_to_upright")
        self.__Add("Lori", "swim_diag_upright")
        self.__Add("Lori", "swing")
        self.__Add("Lori", "warp_in")
        self.__Add("Lori", "warp_out_freefall")
        self.__Add("Lori", "freefall")
        self.__Add("Lori", "warp_in_freefall")
        self.__Add("Lori", "warp_out")
        self.__Add("Lori", "pole_v")
        self.__NextSet()
        self.__Add("Lori", "idle_2")
        self.__Add("Lori", "gun")
        self.__NextSet()
        self.__NextSet()
        self.__Add("UI", "multiplayer_char", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "multiplayer_color")
        self.__Add("UI", "character_art_difficulty_jazz", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_art_difficulty_lori", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_art_difficulty_spaz", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("Unimplemented", "key", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "loading_bar", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "multiplayer_mode", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_name_jazz", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_name_lori", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_name_spaz", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_art_jazz", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_art_lori", palette="Menu.Palette", skipNormalMap=True)
        self.__Add("UI", "character_art_spaz", palette="Menu.Palette", skipNormalMap=True)
        self.__NextSet()

    def __GetSampleMapping(self):
        pass

    def __Add(self, category, name, palette="Std.Palette", skipNormalMap=False, addBorder=0, allowRealtimePalette=False):
        entry = Entry()

        entry.AddBorder = addBorder
        entry.AllowRealtimePalette = allowRealtimePalette
        entry.Category = category
        entry.Name = name
        entry.Palette = palette
        entry.SkipNormalMap = skipNormalMap

        self.tempSet.append(entry)

    def __NextSet(self):
        self.map.append(self.tempSet)
        self.tempSet = []

    def Get(self, setID, animID):
        try:
            return self.map[setID][animID]
        except IndexError:
            entry = Entry()
            entry.Category = "Unidentified"
            entry.Name = str(setID) + "_" + str(animID)
            return entry

    def GetMappingData(self):
        endData = {}

        for x in range(len(self.map)):
            rawSetData = self.map[x]
            setData = {}

            for y in range(len(rawSetData)):
                data = rawSetData[y]
                setData[y] = data.Category + "/" + data.Name

            endData[x] = setData

        return endData


animMapping = AnimSetMapping("anim")
sampleMapping = AnimSetMapping("sample")
