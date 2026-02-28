// Check if building for Electron or in development mode
const isElectronBuild = process.env.BUILD_TARGET === 'electron' || process.argv.includes('--electron');
const isDevelopment = process.env.NODE_ENV !== 'production';

const nextConfig = {
  reactStrictMode: false,
  distDir: ".next-build",
  ...(isElectronBuild ? { output: "export" } : isDevelopment ? {} : { output: "export" }),
  ...(isDevelopment ? { allowedDevOrigins: ['127.0.0.1:*', 'localhost:*'] } : {}),
  
  // Disable font optimization to avoid Google Fonts download warnings during build
  optimizeFonts: false,

  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "pub-7c765f3726084c52bcd5d180d51f1255.r2.dev",
      },
      {
        protocol: "https",
        hostname: "pptgen-public.ap-south-1.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "pptgen-public.s3.ap-south-1.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "img.icons8.com",
      },
      {
        protocol: "https",
        hostname: "present-for-me.s3.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "yefhrkuqbjcblofdcpnr.supabase.co",
      },
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "picsum.photos",
      },
      {
        protocol: "https",
        hostname: "unsplash.com",
      },
    ],
  },
};


export default nextConfig;
