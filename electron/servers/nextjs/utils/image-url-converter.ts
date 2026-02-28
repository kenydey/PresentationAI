/**
 * Converts file:// protocol image URLs to HTTP URLs for Docker/browser compatibility
 * In Electron: file:///app_data/images/... works
 * In Docker/Browser: needs http://localhost/app_data/images/...
 */
export function convertImageUrlsForEnvironment() {
  // Check if we're in Electron environment
  const isElectron = typeof window !== 'undefined' && (window as any).electron;
  
  // If in Electron, file:// URLs work fine, no conversion needed
  if (isElectron) {
    return;
  }
  
  // In Docker/browser, convert all file:// URLs to HTTP URLs
  const images = document.querySelectorAll('img[src^="file://"]');
  
  images.forEach((img) => {
    const htmlImg = img as HTMLImageElement;
    const fileSrc = htmlImg.src;
    
    // Extract the path after file://
    // file:///app_data/images/xxx.png -> /app_data/images/xxx.png
    const match = fileSrc.match(/^file:\/\/(.*)$/);
    if (match) {
      const filePath = match[1];
      // Convert to HTTP URL that goes through nginx
      // In Docker, nginx serves /app_data/images/ from the mounted volume
      htmlImg.src = filePath;
    }
  });
}

/**
 * Setup a MutationObserver to automatically convert any dynamically added images
 */
export function setupImageUrlConverter() {
  convertImageUrlsForEnvironment();
  
  // Watch for dynamically added images
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          const element = node as Element;
          
          // Check if the added node is an img with file:// src
          if (element.tagName === 'IMG' && element.getAttribute('src')?.startsWith('file://')) {
            convertImageUrlsForEnvironment();
          }
          
          // Check for img descendants
          const imgs = element.querySelectorAll?.('img[src^="file://"]');
          if (imgs && imgs.length > 0) {
            convertImageUrlsForEnvironment();
          }
        }
      });
    });
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
  
  return observer;
}
