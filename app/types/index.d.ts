interface FastApiEnv {
  DEBUG: string,
  LLM: string,
  LIBREOFFICE: string,
  OPENAI_API_KEY: string,
  GOOGLE_API_KEY: string,
  APP_DATA_DIRECTORY: string,
  TEMP_DIRECTORY: string,
}

interface NextJsEnv {
  NEXT_PUBLIC_API: string,
  TEMP_DIRECTORY: string,
}