import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
<<<<<<< HEAD

=======
import * as Switch from "@radix-ui/react-switch";
import styles from "../styles/main.module.css";
>>>>>>> 78e1006 (Initial: presenton)

interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
<<<<<<< HEAD

=======
  researchMode: boolean;
  setResearchMode: (value: boolean) => void;
>>>>>>> 78e1006 (Initial: presenton)
}

export function PromptInput({
  value,
  onChange,
<<<<<<< HEAD

=======
  researchMode,
  setResearchMode,
>>>>>>> 78e1006 (Initial: presenton)
}: PromptInputProps) {
  const [showHint, setShowHint] = useState(false);
  const handleChange = (value: string) => {
    setShowHint(value.length > 0);
    onChange(value);
  };
  return (
    <div className="space-y-2">
<<<<<<< HEAD
=======
      <div className="flex justify-between">
        <h4 className=" font-satoshi text-lg text-[#444] font-medium ">
          Prompt
        </h4>
        <div className="flex justify-end">
          <div
            className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-md border border-[#5146E5] text-sm font-semibold ${
              researchMode ? "bg-[#5146E5] text-white" : "text-[#5146E5]"
            }`}
          >
            <span>Research Mode</span>
            <Switch.Root
              defaultChecked={researchMode}
              onCheckedChange={(val) => setResearchMode(val)}
              className={`${styles.SwitchRoot}`}
            >
              <Switch.Thumb className={styles.SwitchThumb} />
            </Switch.Root>
          </div>
        </div>
      </div>
      {researchMode && (
        <p className="bg-blue-100 border font-satoshi text-sm md:text-base transition-all duration-300 border-blue-200 p-2 text-center rounded-md ">
          Research mode searches the web to gather the latest information based
          on your prompt and documents.
        </p>
      )}

>>>>>>> 78e1006 (Initial: presenton)
      <div className="relative">
        <Textarea
          value={value}
          rows={5}
          onChange={(e) => handleChange(e.target.value)}
          placeholder="Tell us about your presentation"
<<<<<<< HEAD
          data-testid="prompt-input"
          className={`py-4 px-5 border-2 font-medium font-instrument_sans text-base min-h-[150px] max-h-[300px] border-[#5146E5] focus-visible:ring-offset-0  focus-visible:ring-[#5146E5] overflow-y-auto  custom_scrollbar  `}
        />
      </div>
      <p
        className={`text-sm text-gray-500 font-inter font-medium ${showHint ? "opacity-100" : "opacity-0"
          }`}
=======
          className={`py-4 px-5 border-2 font-medium text-base min-h-[150px] max-h-[300px] border-[#5146E5] focus-visible:ring-offset-0 font-satoshi focus-visible:ring-[#5146E5] overflow-y-auto  custom_scrollbar  ${
            researchMode ? "border-dashed" : ""
          }`}
        />
      </div>

      <p
        className={`text-sm text-gray-500 font-satoshi font-medium ${
          showHint ? "opacity-100" : "opacity-0"
        }`}
>>>>>>> 78e1006 (Initial: presenton)
      >
        Provide specific details about your presentation needs (e.g., topic,
        style, key points) for more accurate results
      </p>
    </div>
  );
}
