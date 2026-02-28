import { randomChartGenerator } from "@/lib/utils";
import { Slide } from "../types/slide";

const randomGraph = (presentation_id: string) => {
  const randomData = randomChartGenerator();

  return {
    id: crypto.randomUUID(),
    name: "Sales Performance",
    type: "bar",
    presentation: presentation_id,
    postfix: "",
    data: randomData,
  };
};

export const getEmptySlideContent = (
  type: number,
  index: number,
  presentation_id: string
): Slide => {
  const baseSlide: Slide = {
    id: crypto.randomUUID(),
    type,
    index,
    design_index: 1,
    properties: null,
    images: [],
    icons: [],
    graph_id: null,
    presentation: presentation_id,
    content: {
      title: "",
      body: "",
      infographics: [],
    },
  };
  const graph = randomGraph(presentation_id);

  switch (type) {
    case 1:
      return {
        ...baseSlide,
        images: [""],
        content: {
          title: "New Title",
          body: "Add your description here",
          image_prompts: [""],
        },
      };
    case 2:
      return {
        ...baseSlide,
        content: {
          title: "New Title",
          body: [
            { heading: "First Point", description: "Add description" },
            { heading: "Second Point", description: "Add description" },
          ],
        },
      };
    case 4:
      return {
        ...baseSlide,
        images: ["", "", ""],
        content: {
          title: "New Title",
          body: [
            { heading: "First Item", description: "Add description" },
            { heading: "Second Item", description: "Add description" },
            { heading: "Third Item", description: "Add description" },
          ],
          image_prompts: ["", "", ""],
        },
      };
    case 5:
      return {
        ...baseSlide,
        graph_id: graph.id,
        content: {
          graph: graph,
          title: "New Title",
          body: "Add your description here",
        },
      };
    case 6:
      return {
        ...baseSlide,
        content: {
          title: "New Title",
          description: "Add your description here",
          body: [
            { heading: "First Point", description: "Add description" },
            { heading: "Second Point", description: "Add description" },
          ],
        },
      };
    case 7:
      return {
        ...baseSlide,
        icons: ["", "", ""],
        content: {
          title: "New Title",
          body: [
            { heading: "First Point", description: "Add description" },
            { heading: "Second Point", description: "Add description" },
          ],
          icon_queries: [
            {
              queries: [""],
            },
          ],
        },
      };
    case 8:
      return {
        ...baseSlide,
        icons: ["", "", ""],
        content: {
          title: "New Title",
          description: "Add your description here",
          body: [
            { heading: "First Point", description: "Add description" },
            { heading: "Second Point", description: "Add description" },
          ],
          icon_queries: [
            {
              queries: [""],
            },
          ],
        },
      };
    case 9:
      return {
        ...baseSlide,
        graph_id: graph.id,
        content: {
          graph: graph,
          title: "New Subheading",
          body: [
            { heading: "First Point", description: "Add description" },
            { heading: "Second Point", description: "Add description" },
          ],
        },
      };
    case 10:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-ring",
                value: {
                  number_type: "fraction",
                  numerator: 4,
                  denominator: 5,
                },
              },
              description: "Enter Description",
            },
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-ring",
                value: {
                  number_type: "percentage",
                  percentage: 40,
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };
    case 11:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "text",
                value: {
                  number_type: "numerical",
                  numerical: "50",
                  suffix: "quids",
                },
              },
              description: "Enter Description",
            },
            {
              title: "Enter Heading",
              chart: {
                chart_type: "text",
                value: {
                  number_type: "numerical",
                  numerical: "23.4",
                  suffix: "pence",
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };
    case 12:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          description: "Enter Description",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "icon-infographic",
                icon: "hand",
                value: {
                  number_type: "percentage",
                  percentage: 75,
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };
    case 13:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          description: "Enter Description",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "icon-infographic",
                icon: "hand",
                value: {
                  number_type: "percentage",
                  percentage: 75,
                },
              },
              description: "Enter Description",
            },
            {
              title: "Enter Heading",
              chart: {
                chart_type: "icon-infographic",
                icon: "baby",
                value: {
                  number_type: "percentage",
                  percentage: 75,
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };
    case 14:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          description: "Enter Description",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-ring",
                value: {
                  number_type: "percentage",
                  percentage: 40,
                },
              },
              description: "Enter Description",
            },
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-ring",
                value: {
                  number_type: "fraction",
                  numerator: 4,
                  denominator: 5,
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };
    case 15:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          description: "Enter Description",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-dial",
                value: {
                  number_type: "fraction",
                  numerator: 2,
                  denominator: 3,
                },
              },
              description: "Enter Description",
            },
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-dial",
                value: {
                  number_type: "percentage",
                  percentage: 40,
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };

    case 16:
      return {
        ...baseSlide,
        type: 10,
        // @ts-ignore
        content: {
          title: "New Title",
          description: "Enter Description",
          infographics: [
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-bar",
                value: {
                  number_type: "percentage",
                  percentage: 40,
                },
              },
              description: "Enter Description",
            },
            {
              title: "Enter Heading",
              chart: {
                chart_type: "progress-bar",
                value: {
                  number_type: "fraction",
                  numerator: 4,
                  denominator: 5,
                },
              },
              description: "Enter Description",
            },
          ],
        },
      };
    default:
      return baseSlide;
  }
};
