import type { Dispatch, SetStateAction } from "react";
import type { LLMSettings } from "../../hooks/useLLMSettings";

interface Props {

    settings: LLMSettings;

    setSettings: Dispatch<
        SetStateAction<LLMSettings>
    >;

}

export default function MaxTokensSlider({

    settings,

    setSettings,

}: Props) {

    return (

        <div className="playground-field">

            <label>

                Max Tokens

            </label>

            <input

                type="range"

                min={256}

                max={8192}

                step={256}

                value={settings.max_tokens}

                onChange={(e) =>

                    setSettings(prev => ({

                        ...prev,

                        max_tokens: Number(e.target.value),

                    }))

                }

            />

            <span>

                {settings.max_tokens}

            </span>

        </div>

    );

}