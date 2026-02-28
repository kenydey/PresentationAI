/**
 * Fetches text content from a URL or local file path
 * @param url - The URL or file path to fetch content from
 * @returns Promise<string> - The text content
 */
export async function fetchTextFromURL(url: string): Promise<string> {
  console.log('url from here', url);
  if (!url) return "";

  try {
    // Remove file:// prefix if present
    const cleanUrl = url.replace('file://', '');
    
    // If it's a local file path, use the API endpoint
    if (cleanUrl.startsWith('/tmp/') || cleanUrl.startsWith('/')) {
      const response = await fetch('/api/read-file', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filePath: cleanUrl }),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      return data.content;
    }

    // For remote URLs, use regular fetch
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
    }

    return await response.text();
  } catch (error) {
    console.error("Error fetching text:", error);
    return "";
  }
}