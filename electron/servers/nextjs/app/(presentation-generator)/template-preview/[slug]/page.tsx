import GroupLayoutPreview from './components/TemplatePreviewClient';

// Allow dynamic params for custom templates
export const dynamicParams = true;

// Generate static params for built-in template groups
export async function generateStaticParams() {
  // Pre-render built-in template routes at build time
  // Custom templates (custom-*) will be generated on-demand
  return [
    { slug: 'neo-general' },
    { slug: 'neo-standard' },
    { slug: 'neo-modern' },
    { slug: 'general' },
    { slug: 'modern' },
    { slug: 'standard' },
  ];
}

export default function GroupLayoutPreviewPage() {
  return <GroupLayoutPreview />;
}