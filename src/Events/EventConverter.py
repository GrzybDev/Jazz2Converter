from functools import partial

from src.DataClasses.Event import Event
from src.Events.EventParamType import EventParamType
from src.Mappings.Events.EventType import EventType
from src.Mappings.Events.FoodType import FoodType
from src.Mappings.Events.Jazz2Event import Jazz2Event
from src.Mappings.Events.WeaponType import WeaponType


class EventConverter:

    def __init__(self):
        self.converters = {}

        self.__AddDefaultConverters()

    def __Add(self, old, converter):
        if old not in self.converters:
            self.converters[old] = converter
        else:
            raise ValueError("Converter for event " + str(old) + " is already defined!")

    def __AddDefaultConverters(self):
        from src.Events.Converter import Converter

        self.__Add(Jazz2Event.EMPTY, partial(Converter.NoParamList, EventType.Empty))

        # Basic events
        self.__Add(Jazz2Event.JAZZ_LEVEL_START, partial(Converter.ConstantParamList, EventType.LevelStart, 0x01))
        self.__Add(Jazz2Event.SPAZ_LEVEL_START, partial(Converter.ConstantParamList, EventType.LevelStart, 0x02))
        self.__Add(Jazz2Event.LORI_LEVEL_START, partial(Converter.ConstantParamList, EventType.LevelStart, 0x04))

        self.__Add(Jazz2Event.MP_LEVEL_START, partial(Converter.ParamIntToParamList,
                                                      EventType.LevelStartMultiplayer,
                                                      [EventParamType.UInt, 2]))

        self.__Add(Jazz2Event.SAVE_POINT, partial(Converter.SavePoint))

        # Scenery events
        self.__Add(Jazz2Event.SCENERY_DESTRUCT, partial(Converter.SceneryDestructEvent))
        self.__Add(Jazz2Event.SCENERY_DESTR_BOMB, partial(Converter.ConstantParamList, EventType.SceneryDestruct, 7))
        self.__Add(Jazz2Event.SCENERY_BUTTSTOMP, partial(Converter.NoParamList, EventType.SceneryDestructButtstomp))
        self.__Add(Jazz2Event.SCENERY_COLLAPSE, partial(Converter.SceneryCollapse))

        # Modifier events
        self.__Add(Jazz2Event.MODIFIER_HOOK, partial(Converter.NoParamList, EventType.ModifierHook))
        self.__Add(Jazz2Event.MODIFIER_ONE_WAY, partial(Converter.NoParamList, EventType.ModifierOneWay))
        self.__Add(Jazz2Event.MODIFIER_VINE, partial(Converter.NoParamList, EventType.ModifierVine))
        self.__Add(Jazz2Event.MODIFIER_HURT, partial(Converter.ParamIntToParamList,
                                                     EventType.ModifierHurt,
                                                     [EventParamType.Bool, 1],  # Up (JJ2+)
                                                     [EventParamType.Bool, 1],  # Down (JJ2+)
                                                     [EventParamType.Bool, 1],  # Left (JJ2+)
                                                     [EventParamType.Bool, 1]))  # Right (JJ2+)
        self.__Add(Jazz2Event.MODIFIER_RICOCHET, partial(Converter.NoParamList, EventType.ModifierRicochet))
        self.__Add(Jazz2Event.MODIFIER_H_POLE, partial(Converter.NoParamList, EventType.ModifierHPole))
        self.__Add(Jazz2Event.MODIFIER_V_POLE, partial(Converter.NoParamList, EventType.ModifierVPole))
        self.__Add(Jazz2Event.MODIFIER_TUBE, partial(Converter.ModifierTube))
        self.__Add(Jazz2Event.MODIFIER_SLIDE, partial(Converter.ModifierSlide))
        self.__Add(Jazz2Event.MODIFIER_BELT_LEFT, partial(Converter.ModifierBelt, False))
        self.__Add(Jazz2Event.MODIFIER_BELT_RIGHT, partial(Converter.ModifierBelt, True))
        self.__Add(Jazz2Event.MODIFIER_ACC_BELT_LEFT, partial(Converter.ModifierAccBelt, False))
        self.__Add(Jazz2Event.MODIFIER_ACC_BELT_RIGHT, partial(Converter.ModifierAccBelt, True))
        self.__Add(Jazz2Event.MODIFIER_WIND_LEFT, partial(Converter.ModifierWindLeft))
        self.__Add(Jazz2Event.MODIFIER_WIND_RIGHT, partial(Converter.ModifierWindRight))
        self.__Add(Jazz2Event.MODIFIER_SET_WATER, partial(Converter.ModifierSetWater))
        self.__Add(Jazz2Event.AREA_LIMIT_X_SCROLL, partial(Converter.AreaLimitXScroll))

        # Area events
        self.__Add(Jazz2Event.AREA_STOP_ENEMY, partial(Converter.NoParamList, EventType.AreaStopEnemy))
        self.__Add(Jazz2Event.AREA_FLOAT_UP, partial(Converter.NoParamList, EventType.AreaFloatUp))
        self.__Add(Jazz2Event.AREA_ACTIVATE_BOSS, partial(Converter.ParamIntToParamList,
                                                          EventType.AreaActivateBoss,
                                                          [EventParamType.UInt, 1]))  # Music
        self.__Add(Jazz2Event.AREA_EOL, partial(Converter.AreaEOL))
        self.__Add(Jazz2Event.AREA_EOL_WARP, partial(Converter.AreaEOLWarp))
        self.__Add(Jazz2Event.AREA_SECRET_WARP, partial(Converter.AreaSecretWarp))
        self.__Add(Jazz2Event.EOL_SIGN, partial(Converter.EOLSign))
        self.__Add(Jazz2Event.BONUS_SIGN, partial(Converter.ConstantParamList, EventType.AreaEndOfLevel, 3, 0, 0, 0, 0))
        self.__Add(Jazz2Event.AREA_TEXT, partial(Converter.AreaText))
        self.__Add(Jazz2Event.AREA_FLY_OFF, partial(Converter.NoParamList, EventType.AreaFlyOff))
        self.__Add(Jazz2Event.AREA_REVERT_MORPH, partial(Converter.NoParamList, EventType.AreaRevertMorph))
        self.__Add(Jazz2Event.AREA_MORPH_FROG, partial(Converter.NoParamList, EventType.AreaMorphToFrog))
        self.__Add(Jazz2Event.AREA_NO_FIRE, partial(Converter.AreaNoFire))
        self.__Add(Jazz2Event.WATER_BLOCK, partial(Converter.ParamIntToParamList,
                                                   EventType.AreaWaterBlock,
                                                   [EventParamType.Int, 8]))  # Adjust Y
        self.__Add(Jazz2Event.SNOW, partial(Converter.Snow))
        self.__Add(Jazz2Event.AMBIENT_SOUND, partial(Converter.ParamIntToParamList,
                                                     EventType.AreaAmbientSound,
                                                     [EventParamType.UInt, 8],  # Sample
                                                     [EventParamType.UInt, 8],  # Amplify
                                                     [EventParamType.Bool, 1],  # Fade
                                                     [EventParamType.Bool, 1]))  # Sine
        self.__Add(Jazz2Event.SCENERY_BUBBLER, partial(Converter.SceneryBubbler))

        # Trigger Events
        self.__Add(Jazz2Event.TRIGGER_CRATE, partial(Converter.TriggerCrate))
        self.__Add(Jazz2Event.TRIGGER_AREA, partial(Converter.ParamIntToParamList,
                                                    EventType.TriggerArea,
                                                    [EventParamType.UInt, 5]))  # Trigger ID
        self.__Add(Jazz2Event.TRIGGER_ZONE, partial(Converter.ParamIntToParamList,
                                                    EventType.TriggerZone,
                                                    [EventParamType.UInt, 5],  # Trigger ID
                                                    [EventParamType.Bool, 1],  # Set to (0 - off, 1 - on)
                                                    [EventParamType.Bool, 1]))  # Switch
        # Warp Events
        self.__Add(Jazz2Event.WARP_ORIGIN, partial(Converter.WarpOrigin))
        self.__Add(Jazz2Event.WARP_TARGET, partial(Converter.ParamIntToParamList,
                                                   EventType.WarpTarget,
                                                   [EventParamType.UInt, 8]))  # Warp ID

        # Lights
        self.__Add(Jazz2Event.LIGHT_SET, partial(Converter.ParamIntToParamList,
                                                 EventType.LightSet,
                                                 [EventParamType.UInt, 7],  # Intensity
                                                 [EventParamType.UInt, 4],  # Red
                                                 [EventParamType.UInt, 4],  # Green
                                                 [EventParamType.UInt, 4],  # Blue
                                                 [EventParamType.Bool, 1]))  # Flicker
        self.__Add(Jazz2Event.LIGHT_RESET, partial(Converter.NoParamList, EventType.LightReset))
        self.__Add(Jazz2Event.LIGHT_DIM, partial(Converter.ConstantParamList,
                                                 EventType.LightReset,
                                                 127, 60, 100, 0, 0, 0, 0, 0))
        self.__Add(Jazz2Event.LIGHT_STEADY, partial(Converter.LightSteady))
        self.__Add(Jazz2Event.LIGHT_PULSE, partial(Converter.LightPulse))
        self.__Add(Jazz2Event.LIGHT_FLICKER, partial(Converter.LightFlicker))

        # Environment events
        self.__Add(Jazz2Event.PUSHABLE_ROCK, partial(Converter.ConstantParamList,
                                                     EventType.PushableBox,
                                                     0, 0, 0, 0, 0, 0, 0, 0))
        self.__Add(Jazz2Event.PUSHABLE_BOX, partial(Converter.ConstantParamList,
                                                    EventType.PushableBox,
                                                    1, 0, 0, 0, 0, 0, 0, 0))

        self.__Add(Jazz2Event.PLATFORM_FRUIT, partial(Converter.GetPlatformConverter, 1))
        self.__Add(Jazz2Event.PLATFORM_BOLL, partial(Converter.GetPlatformConverter, 2))
        self.__Add(Jazz2Event.PLATFORM_GRASS, partial(Converter.GetPlatformConverter, 3))
        self.__Add(Jazz2Event.PLATFORM_PINK, partial(Converter.GetPlatformConverter, 4))
        self.__Add(Jazz2Event.PLATFORM_SONIC, partial(Converter.GetPlatformConverter, 5))
        self.__Add(Jazz2Event.PLATFORM_SPIKE, partial(Converter.GetPlatformConverter, 6))
        self.__Add(Jazz2Event.BOLL_SPIKE, partial(Converter.GetPlatformConverter, 7))
        self.__Add(Jazz2Event.BOLL_SPIKE_3D, partial(Converter.BallSpike3D))
        self.__Add(Jazz2Event.SPRING_RED, partial(Converter.GetSpringConverter, 0, False, False))
        self.__Add(Jazz2Event.SPRING_GREEN, partial(Converter.GetSpringConverter, 1, False, False))
        self.__Add(Jazz2Event.SPRING_BLUE, partial(Converter.GetSpringConverter, 2, False, False))
        self.__Add(Jazz2Event.SPRING_RED_HOR, partial(Converter.GetSpringConverter, 0, True, False))
        self.__Add(Jazz2Event.SPRING_GREEN_HOR, partial(Converter.GetSpringConverter, 1, True, False))
        self.__Add(Jazz2Event.SPRING_BLUE_HOR, partial(Converter.GetSpringConverter, 2, True, False))
        self.__Add(Jazz2Event.SPRING_GREEN_FROZEN, partial(Converter.GetSpringConverter, 1, False, True))
        self.__Add(Jazz2Event.BRIDGE, partial(Converter.Bridge))
        self.__Add(Jazz2Event.POLE_CARROTUS, partial(Converter.GetPoleConverter, 0))
        self.__Add(Jazz2Event.POLE_DIAMONDUS, partial(Converter.GetPoleConverter, 1))
        self.__Add(Jazz2Event.SMALL_TREE, partial(Converter.GetPoleConverter, 2))
        self.__Add(Jazz2Event.POLE_JUNGLE, partial(Converter.GetPoleConverter, 3))
        self.__Add(Jazz2Event.POLE_PSYCH, partial(Converter.GetPoleConverter, 4))
        self.__Add(Jazz2Event.ROTATING_ROCK, partial(Converter.ParamIntToParamList,
                                                     EventType.RollingRock,
                                                     [EventParamType.UInt, 8],  # ID
                                                     [EventParamType.Int, 4],  # X-Speed
                                                     [EventParamType.Int, 4]))  # Y-Speed
        self.__Add(Jazz2Event.TRIGGER_ROCK, partial(Converter.ParamIntToParamList,
                                                    EventType.RollingRockTrigger,
                                                    [EventParamType.UInt, 8]))  # ID
        self.__Add(Jazz2Event.SWINGING_VINE, partial(Converter.NoParamList, EventType.SwingingVine))

        # Enemies
        self.__Add(Jazz2Event.ENEMY_TURTLE_NORMAL, partial(Converter.ConstantParamList, EventType.EnemyTurtle, 0))
        self.__Add(Jazz2Event.ENEMY_NORMAL_TURTLE_XMAS, partial(Converter.ConstantParamList, EventType.EnemyTurtle, 1))
        self.__Add(Jazz2Event.ENEMY_LIZARD, partial(Converter.ConstantParamList, EventType.EnemyLizard, 0))
        self.__Add(Jazz2Event.ENEMY_LIZARD_XMAS, partial(Converter.ConstantParamList, EventType.EnemyLizard, 1))
        self.__Add(Jazz2Event.ENEMY_LIZARD_FLOAT, partial(Converter.ConstantParamList, EventType.EnemyLizardFloat, 0))
        self.__Add(Jazz2Event.ENEMY_LIZARD_FLOAT_XMAS,
                   partial(Converter.ConstantParamList, EventType.EnemyLizardFloat, 1))
        self.__Add(Jazz2Event.ENEMY_DRAGON, partial(Converter.NoParamList, EventType.EnemyDragon))
        self.__Add(Jazz2Event.ENEMY_LAB_RAT, partial(Converter.NoParamList, EventType.EnemyLabRat))
        self.__Add(Jazz2Event.ENEMY_SUCKER_FLOAT, partial(Converter.NoParamList, EventType.EnemySuckerFloat))
        self.__Add(Jazz2Event.ENEMY_SUCKER, partial(Converter.NoParamList, EventType.EnemySucker))
        self.__Add(Jazz2Event.ENEMY_HELMUT, partial(Converter.NoParamList, EventType.EnemyHelmut))
        self.__Add(Jazz2Event.ENEMY_BAT, partial(Converter.NoParamList, EventType.EnemyBat))
        self.__Add(Jazz2Event.ENEMY_FAT_CHICK, partial(Converter.NoParamList, EventType.EnemyFatChick))
        self.__Add(Jazz2Event.ENEMY_FENCER, partial(Converter.NoParamList, EventType.EnemyFencer))
        self.__Add(Jazz2Event.ENEMY_RAPIER, partial(Converter.NoParamList, EventType.EnemyRapier))
        self.__Add(Jazz2Event.ENEMY_SPARKS, partial(Converter.NoParamList, EventType.EnemySparks))
        self.__Add(Jazz2Event.ENEMY_MONKEY, partial(Converter.ConstantParamList, EventType.EnemyMonkey, 1))
        self.__Add(Jazz2Event.ENEMY_MONKEY_STAND, partial(Converter.ConstantParamList, EventType.EnemyMonkey, 0))
        self.__Add(Jazz2Event.ENEMY_DEMON, partial(Converter.NoParamList, EventType.EnemyDemon))
        self.__Add(Jazz2Event.ENEMY_BEE, partial(Converter.NoParamList, EventType.EnemyBee))
        self.__Add(Jazz2Event.ENEMY_BEE_SWARM, partial(Converter.NoParamList, EventType.EnemyBeeSwarm))
        self.__Add(Jazz2Event.ENEMY_CATERPILLAR, partial(Converter.NoParamList, EventType.EnemyCaterpillar))
        self.__Add(Jazz2Event.ENEMY_CRAB, partial(Converter.NoParamList, EventType.EnemyCrab))
        self.__Add(Jazz2Event.ENEMY_DOGGY_DOGG, partial(Converter.ConstantParamList, EventType.EnemyDoggy, 0))
        self.__Add(Jazz2Event.EMPTY_TSF_DOG, partial(Converter.ConstantParamList, EventType.EnemyDoggy, 1))
        self.__Add(Jazz2Event.ENEMY_DRAGONFLY, partial(Converter.NoParamList, EventType.EnemyDragonfly))
        self.__Add(Jazz2Event.ENEMY_FISH, partial(Converter.NoParamList, EventType.EnemyFish))
        self.__Add(Jazz2Event.ENEMY_MADDER_HATTER, partial(Converter.NoParamList, EventType.EnemyMadderHatter))
        self.__Add(Jazz2Event.ENEMY_RAVEN, partial(Converter.NoParamList, EventType.EnemyRaven))
        self.__Add(Jazz2Event.ENEMY_SKELETON, partial(Converter.NoParamList, EventType.EnemySkeleton))
        self.__Add(Jazz2Event.ENEMY_TUF_TURT, partial(Converter.NoParamList, EventType.EnemyTurtleTough))
        self.__Add(Jazz2Event.ENEMY_TURTLE_TUBE, partial(Converter.NoParamList, EventType.EnemyTurtleTube))
        self.__Add(Jazz2Event.ENEMY_WITCH, partial(Converter.NoParamList, EventType.EnemyWitch))
        self.__Add(Jazz2Event.TURTLE_SHELL, partial(Converter.NoParamList, EventType.TurtleShell))

        # Bosses
        self.__Add(Jazz2Event.BOSS_TWEEDLE, partial(Converter.GetBossConverter, EventType.BossTweedle))
        self.__Add(Jazz2Event.BOSS_BILSY, partial(Converter.GetBossConverter, EventType.BossBilsy, customParam=0))
        self.__Add(Jazz2Event.EMPTY_BOSS_BILSY_XMAS,
                   partial(Converter.GetBossConverter, EventType.BossBilsy, customParam=1))
        self.__Add(Jazz2Event.BOSS_DEVAN_DEVIL, partial(Converter.GetBossConverter, EventType.BossDevan))
        self.__Add(Jazz2Event.BOSS_ROBOT, partial(Converter.NoParamList, EventType.BossRobot))
        self.__Add(Jazz2Event.BOSS_QUEEN, partial(Converter.GetBossConverter, EventType.BossQueen))
        self.__Add(Jazz2Event.BOSS_UTERUS, partial(Converter.GetBossConverter, EventType.BossUterus))
        self.__Add(Jazz2Event.BOSS_BUBBA, partial(Converter.GetBossConverter, EventType.BossBubba))
        self.__Add(Jazz2Event.BOSS_TUF_TURT, partial(Converter.GetBossConverter, EventType.BossTurtleTough))
        self.__Add(Jazz2Event.BOSS_DEVAN_ROBOT, partial(Converter.BossDevanRobot))
        self.__Add(Jazz2Event.BOSS_BOLLY, partial(Converter.GetBossConverter, EventType.BossBolly))

        # Collectibles
        self.__Add(Jazz2Event.COIN_SILVER, partial(Converter.ConstantParamList, EventType.Coin, 0))
        self.__Add(Jazz2Event.COIN_GOLD, partial(Converter.ConstantParamList, EventType.Coin, 1))
        self.__Add(Jazz2Event.GEM_RED, partial(Converter.ConstantParamList, EventType.Gem, 0))
        self.__Add(Jazz2Event.GEM_GREEN, partial(Converter.ConstantParamList, EventType.Gem, 1))
        self.__Add(Jazz2Event.GEM_BLUE, partial(Converter.ConstantParamList, EventType.Gem, 2))
        self.__Add(Jazz2Event.GEM_PURPLE, partial(Converter.ConstantParamList, EventType.Gem, 3))
        self.__Add(Jazz2Event.GEM_RED_RECT, partial(Converter.ConstantParamList, EventType.Gem, 0))
        self.__Add(Jazz2Event.GEM_GREEN_RECT, partial(Converter.ConstantParamList, EventType.Gem, 1))
        self.__Add(Jazz2Event.GEM_BLUE_RECT, partial(Converter.ConstantParamList, EventType.Gem, 2))
        self.__Add(Jazz2Event.GEM_SUPER, partial(Converter.NoParamList, EventType.GemGiant))
        self.__Add(Jazz2Event.GEM_RING, partial(Converter.GemRing))
        self.__Add(Jazz2Event.SCENERY_GEMSTOMP, partial(Converter.NoParamList, EventType.GemStomp))
        self.__Add(Jazz2Event.CARROT, partial(Converter.ConstantParamList, EventType.Carrot, 0))
        self.__Add(Jazz2Event.CARROT_FULL, partial(Converter.ConstantParamList, EventType.Carrot, 1))
        self.__Add(Jazz2Event.CARROT_FLY, partial(Converter.NoParamList, EventType.CarrotFly))
        self.__Add(Jazz2Event.CARROT_INVINCIBLE, partial(Converter.NoParamList, EventType.CarrotInvincible))
        self.__Add(Jazz2Event.ONEUP, partial(Converter.NoParamList, EventType.OneUp))
        self.__Add(Jazz2Event.AMMO_BOUNCER, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.Bouncer))
        self.__Add(Jazz2Event.AMMO_FREEZER, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.Freezer))
        self.__Add(Jazz2Event.AMMO_SEEKER, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.Seeker))
        self.__Add(Jazz2Event.AMMO_RF, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.RF))
        self.__Add(Jazz2Event.AMMO_TOASTER, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.Toaster))
        self.__Add(Jazz2Event.AMMO_TNT, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.TNT))
        self.__Add(Jazz2Event.AMMO_PEPPER, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.Pepper))
        self.__Add(Jazz2Event.AMMO_ELECTRO, partial(Converter.ConstantParamList, EventType.Ammo, WeaponType.Electro))
        self.__Add(Jazz2Event.FAST_FIRE, partial(Converter.NoParamList, EventType.FastFire))
        self.__Add(Jazz2Event.POWERUP_BLASTER,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Blaster))
        self.__Add(Jazz2Event.POWERUP_BOUNCER,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Bouncer))
        self.__Add(Jazz2Event.POWERUP_FREEZER,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Freezer))
        self.__Add(Jazz2Event.POWERUP_SEEKER,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Seeker))
        self.__Add(Jazz2Event.POWERUP_RF, partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.RF))
        self.__Add(Jazz2Event.POWERUP_TOASTER,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Toaster))
        self.__Add(Jazz2Event.POWERUP_TNT,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.TNT))
        self.__Add(Jazz2Event.POWERUP_PEPPER,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Pepper))
        self.__Add(Jazz2Event.POWERUP_ELECTRO,
                   partial(Converter.ConstantParamList, EventType.PowerUpWeapon, WeaponType.Electro))
        self.__Add(Jazz2Event.FOOD_APPLE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Apple))
        self.__Add(Jazz2Event.FOOD_BANANA, partial(Converter.ConstantParamList, EventType.Food, FoodType.Banana))
        self.__Add(Jazz2Event.FOOD_CHERRY, partial(Converter.ConstantParamList, EventType.Food, FoodType.Cherry))
        self.__Add(Jazz2Event.FOOD_ORANGE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Orange))
        self.__Add(Jazz2Event.FOOD_PEAR, partial(Converter.ConstantParamList, EventType.Food, FoodType.Pear))
        self.__Add(Jazz2Event.FOOD_PRETZEL, partial(Converter.ConstantParamList, EventType.Food, FoodType.Pretzel))
        self.__Add(Jazz2Event.FOOD_STRAWBERRY,
                   partial(Converter.ConstantParamList, EventType.Food, FoodType.Strawberry))
        self.__Add(Jazz2Event.FOOD_LEMON, partial(Converter.ConstantParamList, EventType.Food, FoodType.Lemon))
        self.__Add(Jazz2Event.FOOD_LIME, partial(Converter.ConstantParamList, EventType.Food, FoodType.Lime))
        self.__Add(Jazz2Event.FOOD_THING, partial(Converter.ConstantParamList, EventType.Food, FoodType.Thing))
        self.__Add(Jazz2Event.FOOD_WATERMELON,
                   partial(Converter.ConstantParamList, EventType.Food, FoodType.WaterMelon))
        self.__Add(Jazz2Event.FOOD_PEACH, partial(Converter.ConstantParamList, EventType.Food, FoodType.Peach))
        self.__Add(Jazz2Event.FOOD_GRAPES, partial(Converter.ConstantParamList, EventType.Food, FoodType.Grapes))
        self.__Add(Jazz2Event.FOOD_LETTUCE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Lettuce))
        self.__Add(Jazz2Event.FOOD_EGGPLANT, partial(Converter.ConstantParamList, EventType.Food, FoodType.Eggplant))
        self.__Add(Jazz2Event.FOOD_CUCUMBER, partial(Converter.ConstantParamList, EventType.Food, FoodType.Cucumber))
        self.__Add(Jazz2Event.FOOD_PEPSI, partial(Converter.ConstantParamList, EventType.Food, FoodType.Pepsi))
        self.__Add(Jazz2Event.FOOD_COKE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Coke))
        self.__Add(Jazz2Event.FOOD_MILK, partial(Converter.ConstantParamList, EventType.Food, FoodType.Milk))
        self.__Add(Jazz2Event.FOOD_PIE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Pie))
        self.__Add(Jazz2Event.FOOD_CAKE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Cake))
        self.__Add(Jazz2Event.FOOD_DONUT, partial(Converter.ConstantParamList, EventType.Food, FoodType.Donut))
        self.__Add(Jazz2Event.FOOD_CUPCAKE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Cupcake))
        self.__Add(Jazz2Event.FOOD_CHIPS, partial(Converter.ConstantParamList, EventType.Food, FoodType.Chips))
        self.__Add(Jazz2Event.FOOD_CANDY, partial(Converter.ConstantParamList, EventType.Food, FoodType.Candy))
        self.__Add(Jazz2Event.FOOD_CHOCOLATE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Chocolate))
        self.__Add(Jazz2Event.FOOD_ICE_CREAM, partial(Converter.ConstantParamList, EventType.Food, FoodType.IceCream))
        self.__Add(Jazz2Event.FOOD_BURGER, partial(Converter.ConstantParamList, EventType.Food, FoodType.Burger))
        self.__Add(Jazz2Event.FOOD_PIZZA, partial(Converter.ConstantParamList, EventType.Food, FoodType.Pizza))
        self.__Add(Jazz2Event.FOOD_FRIES, partial(Converter.ConstantParamList, EventType.Food, FoodType.Fries))
        self.__Add(Jazz2Event.FOOD_CHICKEN_LEG,
                   partial(Converter.ConstantParamList, EventType.Food, FoodType.ChickenLeg))
        self.__Add(Jazz2Event.FOOD_SANDWICH, partial(Converter.ConstantParamList, EventType.Food, FoodType.Sandwich))
        self.__Add(Jazz2Event.FOOD_TACO, partial(Converter.ConstantParamList, EventType.Food, FoodType.Taco))
        self.__Add(Jazz2Event.FOOD_HOT_DOG, partial(Converter.ConstantParamList, EventType.Food, FoodType.HotDog))
        self.__Add(Jazz2Event.FOOD_HAM, partial(Converter.ConstantParamList, EventType.Food, FoodType.Ham))
        self.__Add(Jazz2Event.FOOD_CHEESE, partial(Converter.ConstantParamList, EventType.Food, FoodType.Cheese))
        self.__Add(Jazz2Event.CRATE_AMMO, partial(Converter.GetAmmoCrateConverter, 0))
        self.__Add(Jazz2Event.CRATE_AMMO_BOUNCER, partial(Converter.GetAmmoCrateConverter, 1))
        self.__Add(Jazz2Event.CRATE_AMMO_FREEZER, partial(Converter.GetAmmoCrateConverter, 2))
        self.__Add(Jazz2Event.CRATE_AMMO_SEEKER, partial(Converter.GetAmmoCrateConverter, 3))
        self.__Add(Jazz2Event.CRATE_AMMO_RF, partial(Converter.GetAmmoCrateConverter, 4))
        self.__Add(Jazz2Event.CRATE_AMMO_TOASTER, partial(Converter.GetAmmoCrateConverter, 5))
        self.__Add(Jazz2Event.CRATE_CARROT,
                   partial(Converter.ConstantParamList, EventType.Crate, EventType.Carrot, 1, 0))
        self.__Add(Jazz2Event.CRATE_SPRING,
                   partial(Converter.ConstantParamList, EventType.Crate, EventType.Spring, 1, 1))
        self.__Add(Jazz2Event.CRATE_ONEUP, partial(Converter.ConstantParamList, EventType.Crate, EventType.OneUp, 1))
        self.__Add(Jazz2Event.CRATE_BOMB, partial(Converter.CrateBomb))
        self.__Add(Jazz2Event.BARREL_AMMO, partial(Converter.ConstantParamList, EventType.BarrelAmmo, 0))
        self.__Add(Jazz2Event.BARREL_CARROT,
                   partial(Converter.ConstantParamList, EventType.Barrel, EventType.Carrot, 1, 0))
        self.__Add(Jazz2Event.BARREL_ONEUP, partial(Converter.ConstantParamList, EventType.Barrel, EventType.OneUp, 1))
        self.__Add(Jazz2Event.CRATE_GEM, partial(Converter.ParamIntToParamList,
                                                 EventType.CrateGem,
                                                 [EventParamType.UInt, 4],  # Red
                                                 [EventParamType.UInt, 4],  # Green
                                                 [EventParamType.UInt, 4],  # Blue
                                                 [EventParamType.UInt, 4]))  # Purple
        self.__Add(Jazz2Event.BARREL_GEM, partial(Converter.ParamIntToParamList,
                                                  EventType.BarrelGem,
                                                  [EventParamType.UInt, 4],  # Red
                                                  [EventParamType.UInt, 4],  # Green
                                                  [EventParamType.UInt, 4],  # Blue
                                                  [EventParamType.UInt, 4]))  # Purple
        self.__Add(Jazz2Event.POWERUP_SWAP, partial(Converter.PowerupSwap))
        self.__Add(Jazz2Event.POWERUP_BIRD, partial(Converter.ConstantParamList, EventType.PowerUpMorph, 2))
        self.__Add(Jazz2Event.BIRDY, partial(Converter.Birdy))

        # Misc events
        self.__Add(Jazz2Event.EVA, partial(Converter.NoParamList, EventType.Eva))
        self.__Add(Jazz2Event.MOTH, partial(Converter.ParamIntToParamList, EventType.Moth, [EventParamType.UInt, 3]))
        self.__Add(Jazz2Event.STEAM, partial(Converter.NoParamList, EventType.SteamNote))
        self.__Add(Jazz2Event.SCENERY_BOMB, partial(Converter.NoParamList, EventType.Bomb))
        self.__Add(Jazz2Event.PINBALL_BUMP_500, partial(Converter.ConstantParamList, EventType.PinballBumper, 0))
        self.__Add(Jazz2Event.PINBALL_BUMP_CARROT, partial(Converter.ConstantParamList, EventType.PinballBumper, 1))
        self.__Add(Jazz2Event.PINBALL_PADDLE_L, partial(Converter.ConstantParamList, EventType.PinballPaddle, 0))
        self.__Add(Jazz2Event.PINBALL_PADDLE_R, partial(Converter.ConstantParamList, EventType.PinballPaddle, 1))
        self.__Add(Jazz2Event.AIRBOARD, partial(Converter.Airboard))
        self.__Add(Jazz2Event.COPTER, partial(Converter.NoParamList, EventType.Copter))
        self.__Add(Jazz2Event.CTF_BASE, partial(Converter.ParamIntToParamList,
                                                EventType.CtfBase,
                                                [EventParamType.UInt, 1],  # Team
                                                [EventParamType.UInt, 1]))  # Direction
        self.__Add(Jazz2Event.SHIELD_FIRE, partial(Converter.ConstantParamList, EventType.PowerUpShield, 1))
        self.__Add(Jazz2Event.SHIELD_WATER, partial(Converter.ConstantParamList, EventType.PowerUpShield, 2))
        self.__Add(Jazz2Event.SHIELD_LIGHTNING, partial(Converter.ConstantParamList, EventType.PowerUpShield, 3))
        self.__Add(Jazz2Event.SHIELD_LASER, partial(Converter.ConstantParamList, EventType.PowerUpShield, 4))
        self.__Add(Jazz2Event.STOPWATCH, partial(Converter.NoParamList, EventType.Stopwatch))

    def Convert(self, level, old, eventParams):
        converter = self.converters.get(old)

        if converter is not None:
            return converter(level=level, params=eventParams)
        else:
            event = Event()
            event.Type = EventType.Empty
            event.Params = None
            return event

    @staticmethod
    def ConvertParamInt(paramInt, paramTypes):
        eventParams = [0 for each in range(len(paramTypes))]

        for index, paramType in enumerate(paramTypes):
            if paramType[1] == 0:
                continue

            if paramType[0] == EventParamType.Bool:
                eventParams[index] = paramInt % 2
                paramInt = paramInt >> 1
            elif paramType[0] == EventParamType.UInt:
                eventParams[index] = paramInt % (1 << paramType[1])
                paramInt = paramInt >> paramType[1]
            elif paramType[0] == EventParamType.Int:
                val = paramInt % (1 << paramType[1] - 1)

                # Complement of two, with variable bit length
                highestBitValue = 1 << (paramType[1] - 1)

                if val >= highestBitValue:
                    val = -highestBitValue + (val - highestBitValue)

                eventParams[index] = val
                paramInt = paramInt >> paramType[1]
            else:
                raise ValueError("Invalid paramType! (" + str(paramType[0]) + ")")

        return eventParams
