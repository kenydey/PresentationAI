<<<<<<< HEAD
import path from "path";

=======
>>>>>>> 78e1006 (Initial: presenton)
export const getIconFromFile = (file: string): string => {
  const file_ext = file.split(".").pop()?.toLowerCase() ?? "";
  if (file_ext == "pdf") {
    return "/pdf.svg";
  } else if (file_ext == "docx") {
    return "/report.png";
  } else if (file_ext == "pptx") {
    return "/ppt.svg";
  }
  return "/report.png";
};

export function isDarkColor(hex: any) {
  // Remove the hash symbol if it's there
  hex = hex.replace("#", "");

  // Convert 3-digit hex to 6-digit
  if (hex.length === 3) {
    hex = hex
      .split("")
      .map((char: any) => char + char)
      .join("");
  }

  // Parse r, g, b values
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);

  // Calculate relative luminance (per WCAG)
  const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;

  // Return true if luminance is below a threshold (dark color)
  return luminance < 128;
}

export function removeUUID(fileName: string) {
  const uuidLength = 36 + 5; // Length of the UUID
  const fileExtensionIndex = fileName.lastIndexOf("."); // Find the last index of file extension

  // Remove the last 36 characters before the file extension
  if (fileExtensionIndex !== -1) {
    return (
      fileName.slice(0, fileName.length - uuidLength) +
      fileName.slice(fileExtensionIndex)
    );
  }

  return fileName; // In case there's no extension
}

<<<<<<< HEAD







export function sanitizeFilename(input: string | null | undefined, replacement = '') {
  // Start with a safe base string to avoid calling string methods on null/undefined
  let sanitized = (input ?? '').toString();
  // Remove any null bytes first
  sanitized = sanitized.replace(/\0/g, '');
  
  // Remove or replace path traversal sequences
  sanitized = sanitized.replace(/\.\./g, replacement);
  
  // Regular filename sanitization (but preserve forward slashes for paths)
  const illegalRe = /[\?<>\\:\*\|"]/g; // Removed / from illegal characters
  const controlRe = /[\x00-\x1f\x80-\x9f]/g;
  const reservedRe = /^\.+$/;
  const windowsReservedRe = /^(con|prn|aux|nul|com\d|lpt\d)$/i;
  const windowsTrailingRe = /[\. ]+$/;

  sanitized = sanitized
    .replace(illegalRe, replacement)
    .replace(controlRe, replacement);

  // Split path into segments to handle reserved names and trailing characters per segment
  const pathSegments = sanitized.split('/');
  const cleanedSegments = pathSegments.map(segment => {
    let cleanSegment = segment
      .replace(reservedRe, replacement)
      .replace(windowsReservedRe, replacement)
      .replace(windowsTrailingRe, replacement);
    
    // Remove any remaining path traversal attempts in individual segments
    cleanSegment = cleanSegment.replace(/\.\./g, replacement);
    
    return cleanSegment;
  });

  sanitized = cleanedSegments.join('/');

  // Remove any remaining path traversal attempts after other replacements
  sanitized = sanitized.replace(/\.\./g, replacement);
  
  // Normalize multiple consecutive slashes to single slash
  sanitized = sanitized.replace(/\/+/g, '/');

  if (sanitized.length === 0) {
    sanitized = 'file';
  }
  // Note: We don't apply MAX_FILENAME_LENGTH to full paths as they can be longer than 255 chars
  // Individual filename components should still be reasonable length

  return sanitized;
}


export function getStaticFileUrl(filepath: string): string {
  const pathParts = filepath.split('/');
  const relevantPath = pathParts.slice(2).join('/');
  return path.join("/static", relevantPath);
}
=======
export const numberTranslations: any = {
  // Key languages
  "English (English)": ["01", "02", "03", "04", "05"],
  "English(English)": ["01", "02", "03", "04", "05"],
  English: ["01", "02", "03", "04", "05"],
  "Spanish (Español)": ["01", "02", "03", "04", "05"],
  "French (Français)": ["01", "02", "03", "04", "05"],
  "German (Deutsch)": ["01", "02", "03", "04", "05"],
  "Portuguese (Português)": ["01", "02", "03", "04", "05"],
  "Italian (Italiano)": ["01", "02", "03", "04", "05"],
  "Dutch (Nederlands)": ["01", "02", "03", "04", "05"],
  "Russian (Русский)": ["01", "02", "03", "04", "05"],
  "Chinese (Simplified & Traditional - 中文, 汉语/漢語)": [
    "一",
    "二",
    "三",
    "四",
    "五",
  ],
  "Japanese (日本語)": ["一", "二", "三", "四", "五"],
  "Korean (한국어)": ["일", "이", "삼", "사", "오"],
  "Arabic (العربية)": ["١", "٢", "٣", "٤", "٥"],
  "Hindi (हिन्दी)": ["०१", "०२", "०३", "०४", "०५"],
  "Bengali (বাংলা)": ["০১", "০২", "০৩", "০৪", "০৫"],

  // European Languages
  "Polish (Polski)": ["01", "02", "03", "04", "05"],
  "Czech (Čeština)": ["01", "02", "03", "04", "05"],
  "Slovak (Slovenčina)": ["01", "02", "03", "04", "05"],
  "Hungarian (Magyar)": ["01", "02", "03", "04", "05"],
  "Romanian (Română)": ["01", "02", "03", "04", "05"],
  "Bulgarian (Български)": ["01", "02", "03", "04", "05"],
  "Greek (Ελληνικά)": ["α΄", "β΄", "γ΄", "δ΄", "ε΄"],
  "Serbian (Српски)": ["01", "02", "03", "04", "05"],
  "Croatian (Hrvatski)": ["01", "02", "03", "04", "05"],
  "Bosnian (Bosanski)": ["01", "02", "03", "04", "05"],
  "Slovenian (Slovenščina)": ["01", "02", "03", "04", "05"],
  "Finnish (Suomi)": ["01", "02", "03", "04", "05"],
  "Swedish (Svenska)": ["01", "02", "03", "04", "05"],
  "Danish (Dansk)": ["01", "02", "03", "04", "05"],
  "Norwegian (Norsk)": ["01", "02", "03", "04", "05"],
  "Icelandic (Íslenska)": ["01", "02", "03", "04", "05"],
  "Lithuanian (Lietuvių)": ["01", "02", "03", "04", "05"],
  "Latvian (Latviešu)": ["01", "02", "03", "04", "05"],
  "Estonian (Eesti)": ["01", "02", "03", "04", "05"],
  "Maltese (Malti)": ["01", "02", "03", "04", "05"],
  "Welsh (Cymraeg)": ["01", "02", "03", "04", "05"],
  "Irish (Gaeilge)": ["01", "02", "03", "04", "05"],
  "Scottish Gaelic (Gàidhlig)": ["01", "02", "03", "04", "05"],

  // Middle Eastern and Central Asian Languages
  "Hebrew (עברית)": ["א׳", "ב׳", "ג׳", "ד׳", "ה׳"],
  "Persian/Farsi (فارسی)": ["۱", "۲", "۳", "۴", "۵"],
  "Turkish (Türkçe)": ["01", "02", "03", "04", "05"],
  "Kurdish (Kurdî / کوردی)": ["١", "٢", "٣", "٤", "٥"],
  "Pashto (پښتو)": ["١", "٢", "٣", "٤", "٥"],
  "Dari (دری)": ["١", "٢", "٣", "٤", "٥"],
  "Uzbek (Oʻzbek)": ["01", "02", "03", "04", "05"],
  "Kazakh (Қазақша)": ["01", "02", "03", "04", "05"],
  "Tajik (Тоҷикӣ)": ["01", "02", "03", "04", "05"],
  "Turkmen (Türkmençe)": ["01", "02", "03", "04", "05"],
  "Azerbaijani (Azərbaycan dili)": ["01", "02", "03", "04", "05"],

  // South Asian Languages
  "Urdu (اردو)": ["١", "٢", "٣", "٤", "٥"],
  "Tamil (தமிழ்)": ["௧", "௨", "௩", "௪", "௫"],
  "Telugu (తెలుగు)": ["౧", "౨", "౩", "౪", "౫"],
  "Marathi (मराठी)": ["०१", "०२", "०३", "०४", "०५"],
  "Punjabi (ਪੰਜਾਬੀ / پنجابی)": ["੦੧", "੦੨", "੦੩", "੦੪", "੦੫"],
  "Gujarati (ગુજરાતી)": ["૦૧", "૦૨", "૦૩", "૦૪", "૦૫"],
  "Malayalam (മലയാളം)": ["൧", "൨", "൩", "൪", "൫"],
  "Kannada (ಕನ್ನಡ)": ["೧", "೨", "೩", "೪", "೫"],
  "Odia (ଓଡ଼ିଆ)": ["୧", "୨", "୩", "୪", "୫"],
  "Sinhala (සිංහල)": ["෧", "෨", "෩", "෪", "෫"],
  "Nepali (नेपाली)": ["०१", "०२", "०३", "०४", "०५"],

  // East and Southeast Asian Languages
  "Thai (ไทย)": ["๑", "๒", "๓", "๔", "๕"],
  "Vietnamese (Tiếng Việt)": ["01", "02", "03", "04", "05"],
  "Lao (ລາວ)": ["໑", "໒", "໓", "໔", "໕"],
  "Khmer (ភាសាខ្មែរ)": ["១", "២", "៣", "៤", "៥"],
  "Burmese (မြန်မာစာ)": ["၁", "၂", "၃", "၄", "၅"],
  "Tagalog/Filipino (Tagalog/Filipino)": ["01", "02", "03", "04", "05"],
  "Javanese (Basa Jawa)": ["01", "02", "03", "04", "05"],
  "Sundanese (Basa Sunda)": ["01", "02", "03", "04", "05"],
  "Malay (Bahasa Melayu)": ["01", "02", "03", "04", "05"],
  "Mongolian (Монгол)": ["01", "02", "03", "04", "05"],

  // African Languages
  "Swahili (Kiswahili)": ["01", "02", "03", "04", "05"],
  "Hausa (Hausa)": ["01", "02", "03", "04", "05"],
  "Yoruba (Yoruba)": ["01", "02", "03", "04", "05"],
  "Igbo (Igbo)": ["01", "02", "03", "04", "05"],
  "Amharic (አማርኛ)": ["፩", "፪", "፫", "፬", "፭"],
  "Zulu (isiZulu)": ["01", "02", "03", "04", "05"],
  "Xhosa (isiXhosa)": ["01", "02", "03", "04", "05"],
  "Shona (ChiShona)": ["01", "02", "03", "04", "05"],
  "Somali (Soomaaliga)": ["01", "02", "03", "04", "05"],

  // Indigenous and Lesser-Known Languages
  "Basque (Euskara)": ["01", "02", "03", "04", "05"],
  "Catalan (Català)": ["01", "02", "03", "04", "05"],
  "Galician (Galego)": ["01", "02", "03", "04", "05"],
  "Quechua (Runasimi)": ["01", "02", "03", "04", "05"],
  "Nahuatl (Nāhuatl)": ["01", "02", "03", "04", "05"],
  "Hawaiian (ʻŌlelo Hawaiʻi)": ["01", "02", "03", "04", "05"],
  "Maori (Te Reo Māori)": ["01", "02", "03", "04", "05"],
  "Tahitian (Reo Tahiti)": ["01", "02", "03", "04", "05"],
  "Samoan (Gagana Samoa)": ["01", "02", "03", "04", "05"],
};

export const ThemeImagePrompt = {
  light:
    "Classy and modern with a corporate and minimalist touch. Tone is serious yet elegant, using a palette of light, white, and cool gray colors.",
  dark: "Luxurious and futuristic with a simple, clean design. Professional yet elegant using a color scheme of dark, black, and high contrast.",
  faint_yellow:
    "Fresh young creatively vibrant style, utilizing a playful mixture of light colors like orange, salmon, and pastel purple, all set against a warm gradient.",
  cream:
    "Elegant with a classic and professional look. Subtle and minimalist using a warm palette of cream, beige, and light beige colors.",
  royal_blue:
    "Playful and creative, bold and loud with a futuristic touch, using a gradient of vibrant colors including blue, purple, and royal blue.",
  light_red:
    "Fun and organic with a playful and inspirational aesthetic, featuring pastel colors like pink, coral, and orange for a vibrant and warm feel.",
  dark_pink:
    " Inspirational and creative with a youthful and playful tone, featuring light, pastel colors including blue, pink, and purple, all blending in a vibrant gradient.",
  custom: "",
};
>>>>>>> 78e1006 (Initial: presenton)
