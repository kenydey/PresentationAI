interface ElementPosition {
  left: number;
  top: number;
  width: number;
  height: number;
}

interface FontStyles {
  name: string;
  size: number;
  weight: string;
  color: string;
}



interface TextMetadata {

  position: ElementPosition;
  paragraphs: Array<{
    text: string;
    font: FontStyles;
  }>;
}

interface PictureMetadata {
  
  position: ElementPosition;
  picture:{
    is_network: boolean;
    path: string;
  }
  border_radius: number;
}

interface GraphMetadata {

  position: ElementPosition;
  categoryFont: FontStyles;
  valueFont: FontStyles;
  legendFont: FontStyles;
  graphData: {
    type: string;
    data: any; // Replace with your specific graph data structure
  };
}

interface FilledBoxMetadata {
 
  position: ElementPosition;
  type: 1 | 5 | 9; // 1 for rectangle, 2 for circle
  fill: {
    color:string;
  };
  stroke:{
    color:string;
    thickness:number;
  },
  shadow:{
    radius:number;
    color:string;
    offset:number;
    opacity:number;
    angle:number;
  },
 
}

interface LineMetadata {
 
  position: ElementPosition;
  lineType: 1;
  thickness: string;
  color: string;
}

interface SlideBoxMetadata {

  position: ElementPosition;

}

type ElementMetadata = TextMetadata | PictureMetadata | GraphMetadata | FilledBoxMetadata | LineMetadata | SlideBoxMetadata;

interface SlideMetadata {
  slideIndex: number;
  backgroundColor:string;
  elements: ElementMetadata[];
}

const FIXED_SLIDE_WIDTH = 1280; // Standard slide width
const FIXED_SLIDE_HEIGHT = 720; // Standard slide height


// Add this helper function before collectSlideMetadata
const  rgbToHex = (color: string): string => {
  // Handle empty or invalid colors
  if (!color || color === 'transparent' || color === 'none') return '#000000';

  // If already hex, return as is
  if (color.startsWith('#')) return color;

  // Extract RGB/RGBA values
  const matches = color.match(/\d+/g);
  if (!matches) return '#000000';

  // Convert to hex
  const r = parseInt(matches[0]);
  const g = parseInt(matches[1]);
  const b = parseInt(matches[2]);
  
  return [r, g, b]
    .map(x => x.toString(16).padStart(2, '0'))
    .join('');
};



export const collectSlideMetadata = (): SlideMetadata[] => {
  const slidesMetadata: SlideMetadata[] = [];
  
  const slideContainers = document.querySelectorAll('[data-element-type="slide-container"]');
  
  slideContainers.forEach((container) => {
    const containerEl = container as HTMLElement;
    const containerRect = containerEl.getBoundingClientRect();
    const slideIndex = parseInt(containerEl.getAttribute('data-slide-index') || '0');
    
    // Get container computed styles
    const containerComputedStyle = window.getComputedStyle(containerEl);
    
    const slideMetadata: SlideMetadata = {
      slideIndex,
      backgroundColor: rgbToHex(containerComputedStyle.backgroundColor),
      elements: []
    };

    const elements = containerEl.querySelectorAll('[data-slide-element]:not([data-element-type="slide-container"])');
    
    elements.forEach((element) => {
      const el = element as HTMLElement;
      const elementRect = el.getBoundingClientRect();
      const computedStyle = window.getComputedStyle(el);

      // Calculate position relative to slide container
      const position: ElementPosition = {
        left: Math.round(elementRect.left - containerRect.left),
      top: Math.round(elementRect.top - containerRect.top),
        width: Math.round(elementRect.width),
        height: Math.round(elementRect.height)
      };
      

      const elementType = el.getAttribute('data-element-type');
      if (!elementType) return;

      // Get computed font styles after Tailwind has been applied
      const fontStyles: FontStyles = {
        // name: computedStyle.fontFamily.replace(/['"]/g, ''),
        name:"Inter",
        size: parseInt(computedStyle.fontSize),
        weight: computedStyle.fontWeight,
        color: rgbToHex(computedStyle.color)
      };

      switch (elementType) {
        case 'text':
          slideMetadata.elements.push({
            position,
            paragraphs: [{
              text: el.textContent || '',
              font: fontStyles
            }]
          });
          break;

        case 'picture':
          // Handle both img elements and elements containing img
          let imgEl: HTMLImageElement | null;
          if (el.tagName.toLowerCase() === 'img') {
            imgEl = el as HTMLImageElement;
          } else {
            imgEl = el.querySelector('img');
          }

          if (imgEl) {
            slideMetadata.elements.push({
              
              position,
              picture:{

                is_network: imgEl.src.startsWith('http'),
                path: imgEl.src || imgEl.getAttribute('data-image-path') || '',
              },
              border_radius: parseInt(computedStyle.borderRadius)
            });
          }
          break;

        case 'graph':
          slideMetadata.elements.push({
            position,
            categoryFont: {
              name: computedStyle.fontFamily.replace(/['"]/g, ''),
              size: parseInt(computedStyle.fontSize)  ,
              weight: computedStyle.fontWeight,
              color: computedStyle.color
            },
            valueFont: fontStyles,
            legendFont: fontStyles,
            graphData: {
              type: el.getAttribute('data-graph-type') || 'bar',
              data: JSON.parse(el.getAttribute('data-graph-data') || '{}')
            }
          });
          break;

        case 'filledbox':{
  const boxShadow = computedStyle.boxShadow;
  
  // Default shadow properties
  let shadowRadius = 0;
  let shadowColor = '#000000';
  let shadowOffsetX = 0;
  let shadowOffsetY = 0;
  let shadowOpacity = 0;

  if (boxShadow && boxShadow !== 'none') {
    // Regex to parse box-shadow values: "offset-x offset-y blur-radius spread-radius color"
      const boxShadowRegex = /rgba?\((\d+),\s*(\d+),\s*(\d+),?\s*([\d.]+)?\)?\s+(-?\d+px)\s+(-?\d+px)\s+(-?\d+px)\s+(-?\d+px)|(-?\d+px)\s+(-?\d+px)\s+(-?\d+px)\s+(-?\d+px)\s+rgba?\((\d+),\s*(\d+),\s*(\d+),?\s*([\d.]+)?\)?/;

  const match = boxShadow.match(boxShadowRegex);

  if (!match) return null;

  // Extract values based on format
  shadowColor =rgbToHex( match[1]
  ? "rgb(" + match[1] + ", " + match[2] + ", " + match[3] + ")"
  : "rgb(" + match[13] + ", " + match[14] + ", " + match[15] + ")");
  shadowOpacity = parseInt(match[4] || match[16] || '1');
  shadowOffsetX = parseInt(match[5] || match[9]);
  shadowOffsetY = parseInt(match[6] || match[10]);
 shadowRadius = parseInt(match[7] || match[11]);

  }

  slideMetadata.elements.push({
    position,
    type: computedStyle.borderRadius === '9999px' || computedStyle.borderRadius === '50%' ? 9 : 5,
    fill: {
      color: rgbToHex(computedStyle.backgroundColor),
    },
    border_radius: parseInt(computedStyle.borderRadius) || 0,
    stroke: {
      color: rgbToHex(computedStyle.borderColor),
      thickness: parseInt(computedStyle.borderWidth) || 0,
    },
    shadow: {
      radius: shadowRadius,
      color: shadowColor,
      offset: Math.sqrt(shadowOffsetX ** 2 + shadowOffsetY ** 2), // Total offset length
      opacity: shadowOpacity,
      angle: Math.round((Math.atan2(shadowOffsetY, shadowOffsetX) * 180) / Math.PI), // Shadow angle in degrees
    },
   
  });
  break;
}

        case 'line':
          slideMetadata.elements.push({
         
            position,
            lineType: 1,
            thickness: computedStyle.borderWidth || computedStyle.height,
            color: rgbToHex(computedStyle.borderColor || computedStyle.backgroundColor)
          });
          break;
       case 'slide-box': {
  const boxShadow = computedStyle.boxShadow;
  console.log('slide-box', boxShadow, 'slide-box');

  // Default shadow properties
  let shadowRadius = 0;
  let shadowColor = '#000000';
  let shadowOffsetX = 0;
  let shadowOffsetY = 0;
  let shadowOpacity = 0;

  if (boxShadow && boxShadow !== 'none') {
    // Regex to parse box-shadow values: "offset-x offset-y blur-radius spread-radius color"
    const boxShadowRegex = /rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)\s*(-?\d+)px\s*(-?\d+)px\s*(-?\d+)px\s*(-?\d+)px/;
    const match = boxShadow.match(boxShadowRegex);

    if (match) {
        const [_, r, g, b, opacity, xOffset, yOffset, blurRadius, spreadRadius] = match;
        console.log('rgb',`rgb(${r},${g},${b})`);
      shadowOpacity=parseInt(opacity);
      shadowRadius=parseInt(blurRadius);
      shadowColor= rgbToHex(`rgba(${r},${g},${b},1)`)
      shadowOffsetX=parseInt(xOffset);

      shadowOffsetY=parseInt(yOffset);

    
    }
  }

  slideMetadata.elements.push({
    position,
    type: computedStyle.borderRadius === '9999px' || computedStyle.borderRadius === '50%' ? 9 : 5,
    fill: {
      color: rgbToHex(computedStyle.backgroundColor),
    },
    border_radius: parseInt(computedStyle.borderRadius) || 0,
    stroke: {
      color: rgbToHex(computedStyle.borderColor),
      thickness: parseInt(computedStyle.borderWidth) || 0,
    },
    shadow: {
      radius: shadowRadius,
      color: shadowColor,
      offset: Math.sqrt(shadowOffsetX ** 2 + shadowOffsetY ** 2), // Total offset length
      opacity: shadowOpacity,
      angle: Math.round((Math.atan2(shadowOffsetY, shadowOffsetX) * 180) / Math.PI), // Shadow angle in degrees
    },
   
  });
  break;
}

         
      }
    });

    slidesMetadata.push(slideMetadata);
  });
  
  return slidesMetadata;
}; 