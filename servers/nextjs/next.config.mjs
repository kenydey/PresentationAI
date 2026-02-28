
const nextConfig = {
  reactStrictMode: false,
  distDir: ".next-build",
  

  // Rewrites: 代理 API/字体等到 FastAPI (支持 Docker/nginx 与本地 uv/pip 模式)
  async rewrites() {
    const apiHost = process.env.FASTAPI_URL || 'http://127.0.0.1:8000';
    const mcpHost = process.env.MCP_URL || 'http://127.0.0.1:8001';
    return [
      { source: '/api/v1/:path*', destination: `${apiHost}/api/v1/:path*` },
      { source: '/docs', destination: `${apiHost}/docs` },
      { source: '/docs/:path*', destination: `${apiHost}/docs/:path*` },
      { source: '/openapi.json', destination: `${apiHost}/openapi.json` },
      { source: '/redoc', destination: `${apiHost}/redoc` },
      { source: '/mcp', destination: `${mcpHost}/mcp` },
      { source: '/mcp/:path*', destination: `${mcpHost}/mcp/:path*` },
      { source: '/app_data/:path*', destination: `${apiHost}/app_data/:path*` },
    ];
  },

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
