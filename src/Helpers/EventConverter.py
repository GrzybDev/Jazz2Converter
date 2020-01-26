from src.DataClasses.Event import Event
from src.Mappings import EventParamType
from src.Mappings.EventType import EventType
from src.Mappings.FoodType import FoodType
from src.Mappings.Jazz2Event import Jazz2Event
from functools import partial

from src.Mappings.WeaponType import WeaponType


class EventConverter:

    def __init__(self):
        self.converters = {}

        self.__AddDefaultConverters()

    def __AddDefaultConverters(self):
        self.__Add(Jazz2Event.EMPTY, partial(self.__NoParamList, EventType.Empty))

        # Basic events
        self.__Add(Jazz2Event.JAZZ_LEVEL_START, partial(self.__ConstantParamList, EventType.LevelStart, 0x01))
        self.__Add(Jazz2Event.SPAZ_LEVEL_START, partial(self.__ConstantParamList, EventType.LevelStart, 0x02))
        self.__Add(Jazz2Event.LORI_LEVEL_START, partial(self.__ConstantParamList, EventType.LevelStart, 0x04))

        self.__Add(Jazz2Event.MP_LEVEL_START, partial(self.__ParamIntToParamList,
                                                      EventType.LevelStartMultiplayer,
                                                      [EventParamType.UInt, 2]))

        self.__Add(Jazz2Event.SAVE_POINT, partial(self.__SavePoint))

        # Scenery events
        self.__Add(Jazz2Event.SCENERY_DESTRUCT, partial(self.__SceneryDestructEvent))
        self.__Add(Jazz2Event.SCENERY_DESTR_BOMB, partial(self.__ConstantParamList, EventType.SceneryDestruct, 7))
        self.__Add(Jazz2Event.SCENERY_BUTTSTOMP, partial(self.__NoParamList, EventType.SceneryDestructButtstomp))
        self.__Add(Jazz2Event.SCENERY_COLLAPSE, partial(self.__SceneryCollapse))

        # Modifier events
        self.__Add(Jazz2Event.MODIFIER_HOOK, partial(self.__NoParamList, EventType.ModifierHook))
        self.__Add(Jazz2Event.MODIFIER_ONE_WAY, partial(self.__NoParamList, EventType.ModifierOneWay))
        self.__Add(Jazz2Event.MODIFIER_VINE, partial(self.__NoParamList, EventType.ModifierVine))
        self.__Add(Jazz2Event.MODIFIER_HURT, partial(self.__ParamIntToParamList,
                                                     EventType.ModifierHurt,
                                                     [EventParamType.Bool, 1],   # Up (JJ2+)
                                                     [EventParamType.Bool, 1],   # Down (JJ2+)
                                                     [EventParamType.Bool, 1],   # Left (JJ2+)
                                                     [EventParamType.Bool, 1]))  # Right (JJ2+)
        self.__Add(Jazz2Event.MODIFIER_RICOCHET, partial(self.__NoParamList, EventType.ModifierRicochet))
        self.__Add(Jazz2Event.MODIFIER_H_POLE, partial(self.__NoParamList, EventType.ModifierHPole))
        self.__Add(Jazz2Event.MODIFIER_V_POLE, partial(self.__NoParamList, EventType.ModifierVPole))
        self.__Add(Jazz2Event.MODIFIER_TUBE, partial(self.__ModifierTube))
        self.__Add(Jazz2Event.MODIFIER_SLIDE, partial(self.__ModifierSlide))
        self.__Add(Jazz2Event.MODIFIER_BELT_LEFT, partial(self.__ModifierBelt, False))
        self.__Add(Jazz2Event.MODIFIER_BELT_RIGHT, partial(self.__ModifierBelt, True))
        self.__Add(Jazz2Event.MODIFIER_ACC_BELT_LEFT, partial(self.__ModifierAccBelt, False))
        self.__Add(Jazz2Event.MODIFIER_ACC_BELT_RIGHT, partial(self.__ModifierAccBelt, True))
        self.__Add(Jazz2Event.MODIFIER_WIND_LEFT, partial(self.__ModifierWindLeft))
        self.__Add(Jazz2Event.MODIFIER_WIND_RIGHT, partial(self.__ModifierWindRight))
        self.__Add(Jazz2Event.MODIFIER_SET_WATER, partial(self.__ModifierSetWater))
        self.__Add(Jazz2Event.AREA_LIMIT_X_SCROLL, partial(self.__AreaLimitXScroll))

        # Area events
        self.__Add(Jazz2Event.AREA_STOP_ENEMY, partial(self.__NoParamList, EventType.AreaStopEnemy))
        self.__Add(Jazz2Event.AREA_FLOAT_UP, partial(self.__NoParamList, EventType.AreaFloatUp))
        self.__Add(Jazz2Event.AREA_ACTIVATE_BOSS, partial(self.__ParamIntToParamList,
                                                          EventType.AreaActivateBoss,
                                                          [EventParamType.UInt, 1]))  # Music
        self.__Add(Jazz2Event.AREA_EOL, partial(self.__AreaEOL))
        self.__Add(Jazz2Event.AREA_EOL_WARP, partial(self.__AreaEOLWarp))
        self.__Add(Jazz2Event.AREA_SECRET_WARP, partial(self.__AreaSecretWarp))
        self.__Add(Jazz2Event.EOL_SIGN, partial(self.__EOLSign))
        self.__Add(Jazz2Event.BONUS_SIGN, partial(self.__ConstantParamList, EventType.AreaEndOfLevel, 3, 0, 0, 0, 0))
        self.__Add(Jazz2Event.AREA_TEXT, partial(self.__AreaText))
        self.__Add(Jazz2Event.AREA_FLY_OFF, partial(self.__NoParamList, EventType.AreaFlyOff))
        self.__Add(Jazz2Event.AREA_REVERT_MORPH, partial(self.__NoParamList, EventType.AreaRevertMorph))
        self.__Add(Jazz2Event.AREA_MORPH_FROG, partial(self.__NoParamList, EventType.AreaMorphToFrog))
        self.__Add(Jazz2Event.AREA_NO_FIRE, partial(self.__AreaNoFire))
        self.__Add(Jazz2Event.WATER_BLOCK, partial(self.__ParamIntToParamList,
                                                   EventType.AreaWaterBlock,
                                                   [EventParamType.Int, 8]))  # Adjust Y
        self.__Add(Jazz2Event.SNOW, partial(self.__Snow))
        self.__Add(Jazz2Event.AMBIENT_SOUND, partial(self.__ParamIntToParamList,
                                                     EventType.AreaAmbientSound,
                                                     [EventParamType.UInt, 8],    # Sample
                                                     [EventParamType.UInt, 8],    # Amplify
                                                     [EventParamType.Bool, 1],    # Fade
                                                     [EventParamType.Bool, 1]))  # Sine
        self.__Add(Jazz2Event.SCENERY_BUBBLER, partial(self.__SceneryBubbler))

        # Trigger Events
        self.__Add(Jazz2Event.TRIGGER_CRATE, partial(self.__TriggerCrate))
        self.__Add(Jazz2Event.TRIGGER_AREA, partial(self.__ParamIntToParamList,
                                                    EventType.TriggerArea,
                                                    [EventParamType.UInt, 5]))  # Trigger ID
        self.__Add(Jazz2Event.TRIGGER_ZONE, partial(self.__ParamIntToParamList,
                                                    EventType.TriggerZone,
                                                    [EventParamType.UInt, 5],  # Trigger ID
                                                    [EventParamType.Bool, 1],  # Set to (0 - off, 1 - on)
                                                    [EventParamType.Bool, 1])) # Switch
        # Warp Events
        self.__Add(Jazz2Event.WARP_ORIGIN, partial(self.__WarpOrigin))
        self.__Add(Jazz2Event.WARP_TARGET, partial(self.__ParamIntToParamList,
                                                   EventType.WarpTarget,
                                                   [EventParamType.UInt, 8]))  # Warp ID

        # Lights
        self.__Add(Jazz2Event.LIGHT_SET, partial(self.__ParamIntToParamList,
                                                 EventType.LightSet,
                                                 [EventParamType.UInt, 7],  # Intensity
                                                 [EventParamType.UInt, 4],  # Red
                                                 [EventParamType.UInt, 4],  # Green
                                                 [EventParamType.UInt, 4],  # Blue
                                                 [EventParamType.Bool, 1])) # Flicker
        self.__Add(Jazz2Event.LIGHT_RESET, partial(self.__NoParamList, EventType.LightReset))
        self.__Add(Jazz2Event.LIGHT_DIM, partial(self.__ConstantParamList,
                                                 EventType.LightReset,
                                                 127, 60, 100, 0, 0, 0, 0, 0))
        self.__Add(Jazz2Event.LIGHT_STEADY, partial(self.__LightSteady))
        self.__Add(Jazz2Event.LIGHT_PULSE, partial(self.__LightPulse))
        self.__Add(Jazz2Event.LIGHT_FLICKER, partial(self.__LightFlicker))

        # Environment events
        self.__Add(Jazz2Event.PUSHABLE_ROCK, partial(self.__ConstantParamList,
                                                     EventType.PushableBox,
                                                     0, 0, 0, 0, 0, 0, 0, 0))
        self.__Add(Jazz2Event.PUSHABLE_BOX, partial(self.__ConstantParamList,
                                                    EventType.PushableBox,
                                                    1, 0, 0, 0, 0, 0, 0, 0))

        self.__Add(Jazz2Event.PLATFORM_FRUIT, partial(self.__GetPlatformConverter, 1))
        self.__Add(Jazz2Event.PLATFORM_BOLL, partial(self.__GetPlatformConverter, 2))
        self.__Add(Jazz2Event.PLATFORM_GRASS, partial(self.__GetPlatformConverter, 3))
        self.__Add(Jazz2Event.PLATFORM_PINK, partial(self.__GetPlatformConverter, 4))
        self.__Add(Jazz2Event.PLATFORM_SONIC, partial(self.__GetPlatformConverter, 5))
        self.__Add(Jazz2Event.PLATFORM_SPIKE, partial(self.__GetPlatformConverter, 6))
        self.__Add(Jazz2Event.BOLL_SPIKE, partial(self.__GetPlatformConverter, 7))
        self.__Add(Jazz2Event.BOLL_SPIKE_3D, partial(self.__BallSpike3D))
        self.__Add(Jazz2Event.SPRING_RED, partial(self.__GetSpringConverter, 0, False, False))
        self.__Add(Jazz2Event.SPRING_GREEN, partial(self.__GetSpringConverter, 1, False, False))
        self.__Add(Jazz2Event.SPRING_BLUE, partial(self.__GetSpringConverter, 2, False, False))
        self.__Add(Jazz2Event.SPRING_RED_HOR, partial(self.__GetSpringConverter, 0, True, False))
        self.__Add(Jazz2Event.SPRING_GREEN_HOR, partial(self.__GetSpringConverter, 1, True, False))
        self.__Add(Jazz2Event.SPRING_BLUE_HOR, partial(self.__GetSpringConverter, 2, True, False))
        self.__Add(Jazz2Event.SPRING_GREEN_FROZEN, partial(self.__GetSpringConverter, 1, False, True))
        self.__Add(Jazz2Event.BRIDGE, partial(self.__Bridge))
        self.__Add(Jazz2Event.POLE_CARROTUS, partial(self.__GetPoleConverter, 0))
        self.__Add(Jazz2Event.POLE_DIAMONDUS, partial(self.__GetPoleConverter, 1))
        self.__Add(Jazz2Event.SMALL_TREE, partial(self.__GetPoleConverter, 2))
        self.__Add(Jazz2Event.POLE_JUNGLE, partial(self.__GetPoleConverter, 3))
        self.__Add(Jazz2Event.POLE_PSYCH, partial(self.__GetPoleConverter, 4))
        self.__Add(Jazz2Event.ROTATING_ROCK, partial(self.__ParamIntToParamList,
                                                     EventType.RollingRock,
                                                     [EventParamType.UInt, 8],  # ID
                                                     [EventParamType.Int, 4],   # X-Speed
                                                     [EventParamType.Int, 4]))  # Y-Speed
        self.__Add(Jazz2Event.TRIGGER_ROCK, partial(self.__ParamIntToParamList,
                                                    EventType.RollingRockTrigger,
                                                    [EventParamType.UInt, 8]))  # ID
        self.__Add(Jazz2Event.SWINGING_VINE, partial(self.__NoParamList, EventType.SwingingVine))

        # Enemies
        self.__Add(Jazz2Event.ENEMY_TURTLE_NORMAL, partial(self.__ConstantParamList, EventType.EnemyTurtle, 0))
        self.__Add(Jazz2Event.ENEMY_NORMAL_TURTLE_XMAS, partial(self.__ConstantParamList, EventType.EnemyTurtle, 1))
        self.__Add(Jazz2Event.ENEMY_LIZARD, partial(self.__ConstantParamList, EventType.EnemyLizard, 0))
        self.__Add(Jazz2Event.ENEMY_LIZARD_XMAS, partial(self.__ConstantParamList, EventType.EnemyLizard, 1))
        self.__Add(Jazz2Event.ENEMY_LIZARD_FLOAT, partial(self.__ConstantParamList, EventType.EnemyLizardFloat, 0))
        self.__Add(Jazz2Event.ENEMY_LIZARD_FLOAT_XMAS, partial(self.__ConstantParamList, EventType.EnemyLizardFloat, 1))
        self.__Add(Jazz2Event.ENEMY_DRAGON, partial(self.__NoParamList, EventType.EnemyDragon))
        self.__Add(Jazz2Event.ENEMY_LAB_RAT, partial(self.__NoParamList, EventType.EnemyLabRat))
        self.__Add(Jazz2Event.ENEMY_SUCKER_FLOAT, partial(self.__NoParamList, EventType.EnemySuckerFloat))
        self.__Add(Jazz2Event.ENEMY_SUCKER, partial(self.__NoParamList, EventType.EnemySucker))
        self.__Add(Jazz2Event.ENEMY_HELMUT, partial(self.__NoParamList, EventType.EnemyHelmut))
        self.__Add(Jazz2Event.ENEMY_BAT, partial(self.__NoParamList, EventType.EnemyBat))
        self.__Add(Jazz2Event.ENEMY_FAT_CHICK, partial(self.__NoParamList, EventType.EnemyFatChick))
        self.__Add(Jazz2Event.ENEMY_FENCER, partial(self.__NoParamList, EventType.EnemyFencer))
        self.__Add(Jazz2Event.ENEMY_RAPIER, partial(self.__NoParamList, EventType.EnemyRapier))
        self.__Add(Jazz2Event.ENEMY_SPARKS, partial(self.__NoParamList, EventType.EnemySparks))
        self.__Add(Jazz2Event.ENEMY_MONKEY, partial(self.__ConstantParamList, EventType.EnemyMonkey, 1))
        self.__Add(Jazz2Event.ENEMY_MONKEY_STAND, partial(self.__ConstantParamList, EventType.EnemyMonkey, 0))
        self.__Add(Jazz2Event.ENEMY_DEMON, partial(self.__NoParamList, EventType.EnemyDemon))
        self.__Add(Jazz2Event.ENEMY_BEE, partial(self.__NoParamList, EventType.EnemyBee))
        self.__Add(Jazz2Event.ENEMY_BEE_SWARM, partial(self.__NoParamList, EventType.EnemyBeeSwarm))
        self.__Add(Jazz2Event.ENEMY_CATERPILLAR, partial(self.__NoParamList, EventType.EnemyCaterpillar))
        self.__Add(Jazz2Event.ENEMY_CRAB, partial(self.__NoParamList, EventType.EnemyCrab))
        self.__Add(Jazz2Event.ENEMY_DOGGY_DOGG, partial(self.__ConstantParamList, EventType.EnemyDoggy, 0))
        self.__Add(Jazz2Event.EMPTY_TSF_DOG, partial(self.__ConstantParamList, EventType.EnemyDoggy, 1))
        self.__Add(Jazz2Event.ENEMY_DRAGONFLY, partial(self.__NoParamList, EventType.EnemyDragonfly))
        self.__Add(Jazz2Event.ENEMY_FISH, partial(self.__NoParamList, EventType.EnemyFish))
        self.__Add(Jazz2Event.ENEMY_MADDER_HATTER, partial(self.__NoParamList, EventType.EnemyMadderHatter))
        self.__Add(Jazz2Event.ENEMY_RAVEN, partial(self.__NoParamList, EventType.EnemyRaven))
        self.__Add(Jazz2Event.ENEMY_SKELETON, partial(self.__NoParamList, EventType.EnemySkeleton))
        self.__Add(Jazz2Event.ENEMY_TUF_TURT, partial(self.__NoParamList, EventType.EnemyTurtleTough))
        self.__Add(Jazz2Event.ENEMY_TURTLE_TUBE, partial(self.__NoParamList, EventType.EnemyTurtleTube))
        self.__Add(Jazz2Event.ENEMY_WITCH, partial(self.__NoParamList, EventType.EnemyWitch))
        self.__Add(Jazz2Event.TURTLE_SHELL, partial(self.__NoParamList, EventType.TurtleShell))

        # Bosses
        self.__Add(Jazz2Event.BOSS_TWEEDLE, partial(self.__GetBossConverter, EventType.BossTweedle))
        self.__Add(Jazz2Event.BOSS_BILSY, partial(self.__GetBossConverter, EventType.BossBilsy, customParam=0))
        self.__Add(Jazz2Event.EMPTY_BOSS_BILSY_XMAS, partial(self.__GetBossConverter, EventType.BossBilsy, customParam=1))
        self.__Add(Jazz2Event.BOSS_DEVAN_DEVIL, partial(self.__GetBossConverter, EventType.BossDevan))
        self.__Add(Jazz2Event.BOSS_ROBOT, partial(self.__NoParamList, EventType.BossRobot))
        self.__Add(Jazz2Event.BOSS_QUEEN, partial(self.__GetBossConverter, EventType.BossQueen))
        self.__Add(Jazz2Event.BOSS_UTERUS, partial(self.__GetBossConverter, EventType.BossUterus))
        self.__Add(Jazz2Event.BOSS_BUBBA, partial(self.__GetBossConverter, EventType.BossBubba))
        self.__Add(Jazz2Event.BOSS_TUF_TURT, partial(self.__GetBossConverter, EventType.BossTurtleTough))
        self.__Add(Jazz2Event.BOSS_DEVAN_ROBOT, partial(self.__BossDevanRobot))
        self.__Add(Jazz2Event.BOSS_BOLLY, partial(self.__GetBossConverter, EventType.BossBolly))

        # Collectibles
        self.__Add(Jazz2Event.COIN_SILVER, partial(self.__ConstantParamList, EventType.Coin, 0))
        self.__Add(Jazz2Event.COIN_GOLD, partial(self.__ConstantParamList, EventType.Coin, 1))
        self.__Add(Jazz2Event.GEM_RED, partial(self.__ConstantParamList, EventType.Gem, 0))
        self.__Add(Jazz2Event.GEM_GREEN, partial(self.__ConstantParamList, EventType.Gem, 1))
        self.__Add(Jazz2Event.GEM_BLUE, partial(self.__ConstantParamList, EventType.Gem, 2))
        self.__Add(Jazz2Event.GEM_PURPLE, partial(self.__ConstantParamList, EventType.Gem, 3))
        self.__Add(Jazz2Event.GEM_RED_RECT, partial(self.__ConstantParamList, EventType.Gem, 0))
        self.__Add(Jazz2Event.GEM_GREEN_RECT, partial(self.__ConstantParamList, EventType.Gem, 1))
        self.__Add(Jazz2Event.GEM_BLUE_RECT, partial(self.__ConstantParamList, EventType.Gem, 2))
        self.__Add(Jazz2Event.GEM_SUPER, partial(self.__NoParamList, EventType.GemGiant))
        self.__Add(Jazz2Event.GEM_RING, partial(self.__GemRing))
        self.__Add(Jazz2Event.SCENERY_GEMSTOMP, partial(self.__NoParamList, EventType.GemStomp))
        self.__Add(Jazz2Event.CARROT, partial(self.__ConstantParamList, EventType.Carrot, 0))
        self.__Add(Jazz2Event.CARROT_FULL, partial(self.__ConstantParamList, EventType.Carrot, 1))
        self.__Add(Jazz2Event.CARROT_FLY, partial(self.__NoParamList, EventType.CarrotFly))
        self.__Add(Jazz2Event.CARROT_INVINCIBLE, partial(self.__NoParamList, EventType.CarrotInvincible))
        self.__Add(Jazz2Event.ONEUP, partial(self.__NoParamList, EventType.OneUp))
        self.__Add(Jazz2Event.AMMO_BOUNCER, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.Bouncer))
        self.__Add(Jazz2Event.AMMO_FREEZER, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.Freezer))
        self.__Add(Jazz2Event.AMMO_SEEKER, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.Seeker))
        self.__Add(Jazz2Event.AMMO_RF, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.RF))
        self.__Add(Jazz2Event.AMMO_TOASTER, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.Toaster))
        self.__Add(Jazz2Event.AMMO_TNT, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.TNT))
        self.__Add(Jazz2Event.AMMO_PEPPER, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.Pepper))
        self.__Add(Jazz2Event.AMMO_ELECTRO, partial(self.__ConstantParamList, EventType.Ammo, WeaponType.Electro))
        self.__Add(Jazz2Event.FAST_FIRE, partial(self.__NoParamList, EventType.FastFire))
        self.__Add(Jazz2Event.POWERUP_BLASTER, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Blaster))
        self.__Add(Jazz2Event.POWERUP_BOUNCER, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Bouncer))
        self.__Add(Jazz2Event.POWERUP_FREEZER, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Freezer))
        self.__Add(Jazz2Event.POWERUP_SEEKER, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Seeker))
        self.__Add(Jazz2Event.POWERUP_RF, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.RF))
        self.__Add(Jazz2Event.POWERUP_TOASTER, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Toaster))
        self.__Add(Jazz2Event.POWERUP_TNT, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.TNT))
        self.__Add(Jazz2Event.POWERUP_PEPPER, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Pepper))
        self.__Add(Jazz2Event.POWERUP_ELECTRO, partial(self.__ConstantParamList, EventType.PowerUpWeapon, WeaponType.Electro))
        self.__Add(Jazz2Event.FOOD_APPLE, partial(self.__ConstantParamList, EventType.Food, FoodType.Apple))
        self.__Add(Jazz2Event.FOOD_BANANA, partial(self.__ConstantParamList, EventType.Food, FoodType.Banana))
        self.__Add(Jazz2Event.FOOD_CHERRY, partial(self.__ConstantParamList, EventType.Food, FoodType.Cherry))
        self.__Add(Jazz2Event.FOOD_ORANGE, partial(self.__ConstantParamList, EventType.Food, FoodType.Orange))
        self.__Add(Jazz2Event.FOOD_PEAR, partial(self.__ConstantParamList, EventType.Food, FoodType.Pear))
        self.__Add(Jazz2Event.FOOD_PRETZEL, partial(self.__ConstantParamList, EventType.Food, FoodType.Pretzel))
        self.__Add(Jazz2Event.FOOD_STRAWBERRY, partial(self.__ConstantParamList, EventType.Food, FoodType.Strawberry))
        self.__Add(Jazz2Event.FOOD_LEMON, partial(self.__ConstantParamList, EventType.Food, FoodType.Lemon))
        self.__Add(Jazz2Event.FOOD_LIME, partial(self.__ConstantParamList, EventType.Food, FoodType.Lime))
        self.__Add(Jazz2Event.FOOD_THING, partial(self.__ConstantParamList, EventType.Food, FoodType.Thing))
        self.__Add(Jazz2Event.FOOD_WATERMELON, partial(self.__ConstantParamList, EventType.Food, FoodType.WaterMelon))
        self.__Add(Jazz2Event.FOOD_PEACH, partial(self.__ConstantParamList, EventType.Food, FoodType.Peach))
        self.__Add(Jazz2Event.FOOD_GRAPES, partial(self.__ConstantParamList, EventType.Food, FoodType.Grapes))
        self.__Add(Jazz2Event.FOOD_LETTUCE, partial(self.__ConstantParamList, EventType.Food, FoodType.Lettuce))
        self.__Add(Jazz2Event.FOOD_EGGPLANT, partial(self.__ConstantParamList, EventType.Food, FoodType.Eggplant))
        self.__Add(Jazz2Event.FOOD_CUCUMBER, partial(self.__ConstantParamList, EventType.Food, FoodType.Cucumber))
        self.__Add(Jazz2Event.FOOD_PEPSI, partial(self.__ConstantParamList, EventType.Food, FoodType.Pepsi))
        self.__Add(Jazz2Event.FOOD_COKE, partial(self.__ConstantParamList, EventType.Food, FoodType.Coke))
        self.__Add(Jazz2Event.FOOD_MILK, partial(self.__ConstantParamList, EventType.Food, FoodType.Milk))
        self.__Add(Jazz2Event.FOOD_PIE, partial(self.__ConstantParamList, EventType.Food, FoodType.Pie))
        self.__Add(Jazz2Event.FOOD_CAKE, partial(self.__ConstantParamList, EventType.Food, FoodType.Cake))
        self.__Add(Jazz2Event.FOOD_DONUT, partial(self.__ConstantParamList, EventType.Food, FoodType.Donut))
        self.__Add(Jazz2Event.FOOD_CUPCAKE, partial(self.__ConstantParamList, EventType.Food, FoodType.Cupcake))
        self.__Add(Jazz2Event.FOOD_CHIPS, partial(self.__ConstantParamList, EventType.Food, FoodType.Chips))
        self.__Add(Jazz2Event.FOOD_CANDY, partial(self.__ConstantParamList, EventType.Food, FoodType.Candy))
        self.__Add(Jazz2Event.FOOD_CHOCOLATE, partial(self.__ConstantParamList, EventType.Food, FoodType.Chocolate))
        self.__Add(Jazz2Event.FOOD_ICE_CREAM, partial(self.__ConstantParamList, EventType.Food, FoodType.IceCream))
        self.__Add(Jazz2Event.FOOD_BURGER, partial(self.__ConstantParamList, EventType.Food, FoodType.Burger))
        self.__Add(Jazz2Event.FOOD_PIZZA, partial(self.__ConstantParamList, EventType.Food, FoodType.Pizza))
        self.__Add(Jazz2Event.FOOD_FRIES, partial(self.__ConstantParamList, EventType.Food, FoodType.Fries))
        self.__Add(Jazz2Event.FOOD_CHICKEN_LEG, partial(self.__ConstantParamList, EventType.Food, FoodType.ChickenLeg))
        self.__Add(Jazz2Event.FOOD_SANDWICH, partial(self.__ConstantParamList, EventType.Food, FoodType.Sandwich))
        self.__Add(Jazz2Event.FOOD_TACO, partial(self.__ConstantParamList, EventType.Food, FoodType.Taco))
        self.__Add(Jazz2Event.FOOD_HOT_DOG, partial(self.__ConstantParamList, EventType.Food, FoodType.HotDog))
        self.__Add(Jazz2Event.FOOD_HAM, partial(self.__ConstantParamList, EventType.Food, FoodType.Ham))
        self.__Add(Jazz2Event.FOOD_CHEESE, partial(self.__ConstantParamList, EventType.Food, FoodType.Cheese))
        self.__Add(Jazz2Event.CRATE_AMMO, partial(self.__GetAmmoCrateConverter, 0))
        self.__Add(Jazz2Event.CRATE_AMMO_BOUNCER, partial(self.__GetAmmoCrateConverter, 1))
        self.__Add(Jazz2Event.CRATE_AMMO_FREEZER, partial(self.__GetAmmoCrateConverter, 2))
        self.__Add(Jazz2Event.CRATE_AMMO_SEEKER, partial(self.__GetAmmoCrateConverter, 3))
        self.__Add(Jazz2Event.CRATE_AMMO_RF, partial(self.__GetAmmoCrateConverter, 4))
        self.__Add(Jazz2Event.CRATE_AMMO_TOASTER, partial(self.__GetAmmoCrateConverter, 5))
        self.__Add(Jazz2Event.CRATE_CARROT, partial(self.__ConstantParamList, EventType.Crate, EventType.Carrot, 1, 0))
        self.__Add(Jazz2Event.CRATE_SPRING, partial(self.__ConstantParamList, EventType.Crate, EventType.Spring, 1, 1))
        self.__Add(Jazz2Event.CRATE_ONEUP, partial(self.__ConstantParamList, EventType.Crate, EventType.OneUp, 1))
        self.__Add(Jazz2Event.CRATE_BOMB, partial(self.__CrateBomb))
        self.__Add(Jazz2Event.BARREL_AMMO, partial(self.__ConstantParamList, EventType.BarrelAmmo, 0))
        self.__Add(Jazz2Event.BARREL_CARROT, partial(self.__ConstantParamList, EventType.Barrel, EventType.Carrot, 1, 0))
        self.__Add(Jazz2Event.BARREL_ONEUP, partial(self.__ConstantParamList, EventType.Barrel, EventType.OneUp, 1))
        self.__Add(Jazz2Event.CRATE_GEM, partial(self.__ParamIntToParamList,
                                                 EventType.CrateGem,
                                                 [EventParamType.UInt, 4],  # Red
                                                 [EventParamType.UInt, 4],  # Green
                                                 [EventParamType.UInt, 4],  # Blue
                                                 [EventParamType.UInt, 4])) # Purple
        self.__Add(Jazz2Event.BARREL_GEM, partial(self.__ParamIntToParamList,
                                                  EventType.BarrelGem,
                                                  [EventParamType.UInt, 4],  # Red
                                                  [EventParamType.UInt, 4],  # Green
                                                  [EventParamType.UInt, 4],  # Blue
                                                  [EventParamType.UInt, 4])) # Purple
        self.__Add(Jazz2Event.POWERUP_SWAP, partial(self.__PowerupSwap))
        self.__Add(Jazz2Event.POWERUP_BIRD, partial(self.__ConstantParamList, EventType.PowerUpMorph, 2))
        self.__Add(Jazz2Event.BIRDY, partial(self.__Birdy))

        # Misc events
        self.__Add(Jazz2Event.EVA, partial(self.__NoParamList, EventType.Eva))
        self.__Add(Jazz2Event.MOTH, partial(self.__ParamIntToParamList, EventType.Moth, [EventParamType.UInt, 3]))
        self.__Add(Jazz2Event.STEAM, partial(self.__NoParamList, EventType.SteamNote))
        self.__Add(Jazz2Event.SCENERY_BOMB, partial(self.__NoParamList, EventType.Bomb))
        self.__Add(Jazz2Event.PINBALL_BUMP_500, partial(self.__ConstantParamList, EventType.PinballBumper, 0))
        self.__Add(Jazz2Event.PINBALL_BUMP_CARROT, partial(self.__ConstantParamList, EventType.PinballBumper, 1))
        self.__Add(Jazz2Event.PINBALL_PADDLE_L, partial(self.__ConstantParamList, EventType.PinballPaddle, 0))
        self.__Add(Jazz2Event.PINBALL_PADDLE_R, partial(self.__ConstantParamList, EventType.PinballPaddle, 1))
        self.__Add(Jazz2Event.AIRBOARD, partial(self.__Airboard))
        self.__Add(Jazz2Event.COPTER, partial(self.__NoParamList, EventType.Copter))
        self.__Add(Jazz2Event.CTF_BASE, partial(self.__ParamIntToParamList,
                                                EventType.CtfBase,
                                                [EventParamType.UInt, 1],   # Team
                                                [EventParamType.UInt, 1]))  # Direction
        self.__Add(Jazz2Event.SHIELD_FIRE, partial(self.__ConstantParamList, EventType.PowerUpShield, 1))
        self.__Add(Jazz2Event.SHIELD_WATER, partial(self.__ConstantParamList, EventType.PowerUpShield, 2))
        self.__Add(Jazz2Event.SHIELD_LIGHTNING, partial(self.__ConstantParamList, EventType.PowerUpShield, 3))
        self.__Add(Jazz2Event.SHIELD_LASER, partial(self.__ConstantParamList, EventType.PowerUpShield, 4))
        self.__Add(Jazz2Event.STOPWATCH, partial(self.__NoParamList, EventType.Stopwatch))

    def __Add(self, old, converter):
        if old not in self.converters:
            self.converters[old] = converter
        else:
            raise ValueError("Converter for event " + str(old) + " is already defined!")

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

    def __NoParamList(self, ev, level, params):
        event = Event()
        event.Type = ev
        event.Params = None
        return event

    def __ConstantParamList(self, ev, *eventParams, level, params):
        event = Event()
        event.Type = ev
        event.Params = [param for param in eventParams]
        return event

    def __ParamIntToParamList(self, ev, *paramDefs, level, params):
        paramDefs = [param for param in paramDefs]
        eventParams = self.ConvertParamInt(params, paramDefs)

        event = Event()
        event.Type = ev
        event.Params = eventParams
        return event

    def __GetPlatformConverter(self, type, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 2],   # Sync
                                                    [EventParamType.Int, 6],    # Speed
                                                    [EventParamType.UInt, 4],   # Length
                                                    [EventParamType.Bool, 1]])  # Swing
        event = Event()
        event.Type = EventType.MovingPlatform
        event.Params = [type, eventParams[0], eventParams[1], eventParams[2], eventParams[3], 0, 0, 0]
        return event

    def __GetSpringConverter(self, type, horizontal, frozen, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.Bool, 1],  # Orientation (vertical only)
                                                    [EventParamType.Bool, 1],  # Keep X Speed (vertical only)
                                                    [EventParamType.Bool, 1],  # Keep Y Speed
                                                    [EventParamType.UInt, 4],  # Delay
                                                    [EventParamType.Bool, 1]]) # Reverse (horizontal only)

        event = Event()
        event.Type = EventType.Spring
        event.Params = [type, (5 if eventParams[4] != 0 else 4) if horizontal else eventParams[0] * 2,
                        eventParams[1], eventParams[2], eventParams[3], 1 if frozen else 0, 0, 0]
        return event

    def __GetPoleConverter(self, theme, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 5],  # Adjust X
                                                    [EventParamType.Int, 6]])  # Adjust Y

        AdjustX, AdjustY = (2, 2)
        x, y = (eventParams[1] + 16 - AdjustX, (24 if eventParams[0] == 0 else eventParams[0]) - AdjustY)

        event = Event()
        event.Type = EventType.Pole
        event.Params = [theme, x, y]
        return event

    def __GetBossConverter(self, ev, level, params, customParam=0):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 4]])  # EndText

        event = Event()
        event.Type = ev
        event.Params = [customParam, eventParams[0], 0, 0, 0, 0, 0, 0]
        return event

    def __GetAmmoCrateConverter(self, Type, level, params):
        event = Event()
        event.Type = EventType.CrateAmmo
        event.Params = [Type, 0, 0, 0, 0, 0, 0, 0]
        return event

    def __SavePoint(self, level, params):
        theme = 1 if level.tileset.find("xmas") != -1 else 0

        event = Event()
        event.Type = EventType.Checkpoint
        event.Params = [theme, 0]
        return event

    def __SceneryDestructEvent(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Empty
                                                    [EventParamType.UInt, 5],   # Speed
                                                    [EventParamType.UInt, 4]])  # Weapon
        event = Event()

        if eventParams[1] > 0:
            event.Type = EventType.SceneryDestructSpeed
            event.Params = [eventParams[1]]
        else:
            event.Type = EventType.SceneryDestruct
            event.Params = [eventParams[2]]

        return event

    def __SceneryCollapse(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Wait time
                                                    [EventParamType.UInt, 5]])  # FPS

        event = Event()
        event.Type = EventType.SceneryCollapse
        event.Params = [eventParams[0] * 25, eventParams[1]]
        return event

    def __ModifierTube(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.Int, 7],    # X Speed
                                                    [EventParamType.Int, 7],    # Y Speed
                                                    [EventParamType.UInt, 1],   # Trig Sample
                                                    [EventParamType.Bool, 1],   # BecomeNoClip (JJ2+)
                                                    [EventParamType.Bool, 1],   # Noclip Only (JJ2+)
                                                    [EventParamType.UInt, 3]])  # Wait Time (JJ2+)

        event = Event()
        event.Type = EventType.ModifierTube
        event.Params = [eventParams[0], eventParams[1], eventParams[5], eventParams[2], eventParams[3], eventParams[4]]
        return event

    def __ModifierSlide(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 2]])  # Strength

        event = Event()
        event.Type = EventType.ModifierSlide
        event.Params = [eventParams[0]]
        return event

    def __ModifierBelt(self, isRight, level, params):
        if params == 0:
            left = 3 if not isRight else 0
            right = 3 if isRight else 0
        elif params > 127:
            left = 0 if not isRight else 256 - params
            right = 0 if isRight else 256 - params
        else:
            left = params if not isRight else 0
            right = params if isRight else 0

        event = Event()
        event.Type = EventType.AreaHForce
        event.Params = [left, right, 0, 0, 0, 0, 0, 0]
        return event

    def __ModifierAccBelt(self, isRight, level, params):
        if params == 0:
            params = 3

        event = Event()
        event.Type = EventType.AreaHForce
        event.Params = [0, 0, params if not isRight else 0, params if isRight else 0, 0, 0, 0, 0]
        return event

    def __ModifierWindLeft(self, level, params):
        if params > 127:
            left = 256 - params
            right = 0
        else:
            left = 0
            right = params

        event = Event()
        event.Type = EventType.AreaHForce
        event.Params = [0, 0, 0, 0, left, right, 0, 0]
        return event

    def __ModifierWindRight(self, level, params):
        event = Event()
        event.Type = EventType.AreaHForce
        event.Params = [0, 0, 0, 0, 0, params, 0, 0]
        return event

    def __ModifierSetWater(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Height (Tiles)
                                                    [EventParamType.Bool, 1],  # Instant
                                                    [EventParamType.UInt, 2]]) # Lightning

        event = Event()
        event.Type = EventType.ModifierSetWater
        event.Params = [eventParams[0] * 32, eventParams[1], eventParams[2], 0, 0, 0, 0, 0]
        return event

    def __AreaLimitXScroll(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Left (Tiles)
                                                    [EventParamType.UInt, 10]]) # Right (Tiles)
        event = Event()
        event.Type = EventType.ModifierLimitCameraView
        event.Params = [eventParams[0], eventParams[1], 0, 0, 0, 0, 0, 0]
        return event

    def __AreaEOL(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.Bool, 1],  # Secret
                                                    [EventParamType.Bool, 1],  # Fast (JJ2+)
                                                    [EventParamType.UInt, 4],  # TextID (JJ2+)
                                                    [EventParamType.UInt, 4]]) # Offset (JJ2+)

        if eventParams[2] != 0:
            level.AddLevelTokenTextID(eventParams[2])

        event = Event()
        event.Type = EventType.AreaEndOfLevel
        event.Params = [4 if eventParams[0] == 1 else 1, eventParams[1], eventParams[2], eventParams[3], 0]
        return event

    def __AreaEOLWarp(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.Bool, 1],  # Empty (JJ2+)
                                                    [EventParamType.Bool, 1],  # Fast (JJ2+)
                                                    [EventParamType.UInt, 4],  # TextID (JJ2+)
                                                    [EventParamType.UInt, 4]]) # Offset (JJ2+)

        if eventParams[2] != 0:
            level.AddLevelTokenTextID(eventParams[2])

        event = Event()
        event.Type = EventType.AreaEndOfLevel
        event.Params = [2, eventParams[1], eventParams[2], eventParams[3], 0]
        return event

    def __AreaSecretWarp(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 10],  # Coins
                                                    [EventParamType.UInt, 4],   # TextID (JJ2+)
                                                    [EventParamType.UInt, 4]])  # Offset (JJ2+)

        if eventParams[1] != 0:
            level.AddLevelTokenTextID(eventParams[1])

        event = Event()
        event.Type = EventType.AreaEndOfLevel
        event.Params = [3, 0, eventParams[1], eventParams[2], eventParams[0]]
        return event

    def __EOLSign(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.Bool, 1]])  # Secret

        event = Event()
        event.Type = EventType.SignEOL
        event.Params = [4 if eventParams[0] == 1 else 1, 0, 0, 0, 0]
        return event

    def __AreaText(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Text
                                                    [EventParamType.Bool, 1],  # Vanish
                                                    [EventParamType.Bool, 1],  # AngelScript (JJ2+)
                                                    [EventParamType.UInt, 8]]) # Offset (JJ2+)
        event = Event()
        event.Type = EventType.AreaCallback if eventParams[2] != 0 else EventType.AreaText
        event.Params = [eventParams[0], eventParams[3], eventParams[1]]
        return event

    def __AreaNoFire(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 2],  # Set To (JJ2+)
                                                    [EventParamType.UInt, 2]]) # Var (JJ2+)

        event = Event()
        event.Type = EventType.AreaNoFire
        event.Params = [eventParams[0], eventParams[1], eventParams[2]]
        return event

    def __Snow(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 2],  # Intensity
                                                    [EventParamType.Bool, 1],  # Outdoors
                                                    [EventParamType.Bool, 1],  # Off
                                                    [EventParamType.UInt, 2]]) # Type
        event = Event()
        event.Type = EventType.AreaWeather
        event.Params = [0 if eventParams[2] == 1 else eventParams[3] + 1, (eventParams[0] + 1) * 5 / 3, eventParams[1], 0, 0, 0, 0, 0]
        return event

    def __SceneryBubbler(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 4]])  # Speed

        event = Event()
        event.Type = EventType.AreaAmbientBubbles
        event.Params = [(eventParams[0] + 1) * 5 / 3, 0, 0, 0, 0, 0, 0, 0]
        return event

    def __TriggerCrate(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 5],   # Trigger ID
                                                    [EventParamType.Bool, 1],   # Set to (0 - off, 1 - on)
                                                    [EventParamType.Bool, 1]])  # Switch

        event = Event()
        event.Type = EventType.TriggerCrate
        event.Params = [eventParams[0], 1 if eventParams[0] == 0 else 0, eventParams[2]]
        return event

    def __WarpOrigin(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 8],   # Warp ID
                                                    [EventParamType.UInt, 8],   # Coins
                                                    [EventParamType.Bool, 1],   # Set Lap
                                                    [EventParamType.Bool, 1],   # Show
                                                    [EventParamType.Bool, 1]])  # Fast (JJ2+)

        event = Event()
        if eventParams[1] > 0 or eventParams[3] != 0:
            event.Type = EventType.WarpCoinBonus
            event.Params = [eventParams[0], eventParams[4], eventParams[2], eventParams[1], eventParams[3]]
        else:
            event.Type = EventType.WarpOrigin
            event.Params = [eventParams[0], eventParams[4], eventParams[2]]

        return event

    def __LightSteady(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 3],  # Type
                                                    [EventParamType.UInt, 7]]) # Size

        event = Event()
        if eventParams[0] == 1:  # Single point (ignores the "Size" parameter)
            event.Type = EventType.LightSteady
            event.Params = [127, 10, 0, 16, 0, 0, 0, 0]
        elif eventParams[0] == 2:  # Single point (brighter) (ignores the "Size" parameter)
            event.Type = EventType.LightSteady
            event.Params = [255, 200, 0, 16, 0, 0, 0, 0]
        elif eventParams[0] == 3:  # Flicker light
            radiusNear = 60 if eventParams[1] == 0 else eventParams[1] * 6
            radiusFar = radiusNear * 1.666

            event.Type = EventType.LightFlicker
            event.Params = [min(110 + eventParams[1] * 2, 255), 40, radiusNear, radiusFar, 0, 0, 0, 0]
        elif eventParams[0] == 4:  # Bright normal light
            radiusNear = 80 if eventParams[1] == 0 else eventParams[1] * 7
            radiusFar = radiusNear * 1.25

            event.Type = EventType.LightFlicker
            event.Params = [255, 200, radiusNear, radiusFar, 0, 0, 0, 0]
        elif eventParams[0] == 5:  # Laser shield/Illuminate Surroundings
            event.Type = EventType.LightIlluminate
            event.Params = [1 if eventParams[1] < 1 else eventParams[1], 0, 0, 0, 0, 0, 0, 0]
        else:  # Normal
            radiusNear = 60 if eventParams[1] == 0 else eventParams[1] * 6
            radiusFar = radiusNear * 1.666

            event.Type = EventType.LightSteady
            event.Params = [255, 10, radiusNear, radiusFar, 0, 0, 0, 0]

        return event

    def __LightPulse(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 8],  # Speed
                                                    [EventParamType.UInt, 4],  # Sync
                                                    [EventParamType.UInt, 3],  # Type
                                                    [EventParamType.UInt, 5]]) # Size

        radiusNear1 = 20 if eventParams[3] == 0 else eventParams[3] * 4.8
        radiusNear2 = radiusNear1 * 2
        radiusFar = radiusNear1 * 2.4
        speed = 6 if eventParams[0] == 0 else eventParams[0]
        sync = eventParams[1]

        event = Event()

        if eventParams[2] == 4:  # Bright normal light
            event.Type = EventType.LightPulse
            event.Params = [255, 200, radiusNear1, radiusNear2, radiusFar, speed, sync, 0]
        elif eventParams[2] == 5:  # Laser shield/Illuminate Surroundings
            event.Type = EventType.LightIlluminate
            event.Params = [1 if eventParams[1] < 1 else eventParams[1], 0, 0, 0, 0, 0, 0, 0]
        else:  # Normal
            event.Type = EventType.LightPulse
            event.Params = [255, 10, radiusNear1, radiusNear2, radiusFar, speed, sync, 0]

        return event

    def __LightFlicker(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 8]])  # Sample

        event = Event()
        event.Type = EventType.LightFlicker
        event.Params = [110, 40, 60, 110, 0, 0, 0, 0]
        return event

    def __BallSpike3D(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 2],   # Sync
                                                    [EventParamType.Int, 6],    # Speed
                                                    [EventParamType.UInt, 4],   # Length
                                                    [EventParamType.Bool, 1],   # Swing
                                                    [EventParamType.Bool, 1]])  # Shade

        event = Event()
        event.Type = EventType.SpikeBall
        event.Params = [eventParams[0], eventParams[1], eventParams[2], eventParams[3], eventParams[4]]
        return event

    def __Bridge(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 4],  # Width
                                                    [EventParamType.UInt, 3],  # Type
                                                    [EventParamType.UInt, 4]]) # Toughness
        event = Event()
        event.Type = EventType.Bridge
        event.Params = [eventParams[0] * 2, eventParams[1], eventParams[2], 0, 0, 0, 0, 0]
        return event

    def __BossDevanRobot(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 4],  # IntroText
                                                    [EventParamType.UInt, 4]]) # EndText
        event = Event()
        event.Type = EventType.BossDevanRemote
        event.Params = [0, eventParams[0], eventParams[1], 0, 0, 0, 0, 0]
        return event

    def __GemRing(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 5],  # Length
                                                    [EventParamType.UInt, 5],  # Speed
                                                    [EventParamType.Bool, 8]]) # Event
        event = Event()
        event.Type = EventType.GemRing
        event.Params = [eventParams[0], eventParams[1]]
        return event

    def __CrateBomb(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 8],  # ExtraEvent
                                                    [EventParamType.UInt, 4],  # NumEvent
                                                    [EventParamType.Bool, 1],  # RandomFly
                                                    [EventParamType.Bool, 1]]) # NoBomb

        event = Event()
        event.Type = EventType.Crate
        if eventParams[0] > 0 and eventParams[1] > 0:
            event.Params = [eventParams[0], eventParams[1]]
        elif eventParams[3] == 0:
            event.Params = [int(EventType.Bomb), 1]
        else:
            event.Params = [0, 0]
        return event

    def __PowerupSwap(self, level, params):
        event = Event()
        event.Type = EventType.PowerUpMorph
        event.Params = [1]
        return event

    def __Birdy(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.Bool, 1]])  # Chuck (Yellow)

        event = Event()
        event.Type = EventType.BirdCage
        event.Params = [eventParams[0], 0]
        return event

    def __Airboard(self, level, params):
        eventParams = self.ConvertParamInt(params, [[EventParamType.UInt, 5]])  # Delay - Default: 30 (sec)

        event = Event()
        event.Type = EventType.AirboardGenerator
        event.Params = [30 if eventParams[0] == 0 else eventParams[0], 0, 0, 0, 0, 0, 0, 0]
        return event
