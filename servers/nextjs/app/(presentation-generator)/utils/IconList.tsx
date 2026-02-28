import BabyIcon from "@/components/icons/Baby";
import PersonIcon from "@/components/icons/Person";
import HandIcon from "@/components/icons/Hand";
import TreeIcon from "@/components/icons/Tree";
import StarIcon from "@/components/icons/Star";
import CornIcon from "@/components/icons/Corn";
import MealIcon from "@/components/icons/Meal";
import DrinkBottleIcon from "@/components/icons/DrinkBottle";
import CupIcon from "@/components/icons/Cup";
import DropletIcon from "@/components/icons/Droplet";
import HouseIcon from "@/components/icons/House";
import BuildingIcon from "@/components/icons/Building";
import TentIcon from "@/components/icons/Tent";
import CarIcon from "@/components/icons/Car";
import BicycleIcon from "@/components/icons/Bicycle";
import ClockIcon from "@/components/icons/Clock";
import BanknoteIcon from "@/components/icons/Banknote";
import BriefcaseIcon from "@/components/icons/Briefcase";
import TruckIcon from "@/components/icons/Truck";
import AirplaneIcon from "@/components/icons/Airplane";
import LaptopIcon from "@/components/icons/Laptop";
import MobilePhoneIcon from "@/components/icons/MobilePhone";
import LightBulbIcon from "@/components/icons/LightBulb";
import SpannerIcon from "@/components/icons/Spanner";
import FireIcon from "@/components/icons/Fire";
import MortarboardIcon from "@/components/icons/Mortarboard";
import BookIcon from "@/components/icons/Book";
import SyringeIcon from "@/components/icons/Syringe";
import FirstAidIcon from "@/components/icons/FirstAid";
import GlobeIcon from "@/components/icons/Globe";
// First, let's create a constant object with all the icon mappings
export const ICON_LIST = {
  person: PersonIcon,
  female_person: PersonIcon,
  male_person: PersonIcon,
  baby: BabyIcon,
  hand: HandIcon,
  tree: TreeIcon,
  star: StarIcon,
  corn: CornIcon,
  meal: MealIcon,
  drink_bottle: DrinkBottleIcon,
  cup: CupIcon,
  droplet: DropletIcon,
  house: HouseIcon,
  building: BuildingIcon,
  tent: TentIcon,
  car: CarIcon,
  bicycle: BicycleIcon,
  clock: ClockIcon,
  banknote: BanknoteIcon,
  briefcase: BriefcaseIcon,
  truck: TruckIcon,
  airplane: AirplaneIcon,
  laptop_computer: LaptopIcon,
  mobile_phone: MobilePhoneIcon,
  light_bulb: LightBulbIcon,
  spanner: SpannerIcon,
  fire: FireIcon,
  mortarboard: MortarboardIcon,
  book: BookIcon,
  syringe: SyringeIcon,
  first_aid: FirstAidIcon,
  globe: GlobeIcon,
} as const;

// Then modify IconMapper to use this list
export const IconMapper = (isMini = false, icon: string) => {
  const IconComponent = ICON_LIST[icon as keyof typeof ICON_LIST];
  if (!IconComponent) return null;
  return <IconComponent className={isMini ? "w-4 h-4" : "w-12 h-12"} />;
};

export const getPercentage = (numerator: number, denominator: number) => {
  if (denominator === 0) return 0;

  return Math.round((numerator / denominator) * 100);
};
