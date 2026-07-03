import type { Dispatch, SetStateAction } from "react";
import type { LLMSettings } from "../../hooks/useLLMSettings";

interface Props {

    settings: LLMSettings;

    setSettings: Dispatch<
        SetStateAction<LLMSettings>
    >;

}

export default function TemperatureSlider({

    settings,

    setSettings,

}: Props) {

    return (

        <div className="playground-field">

            <label>

                Temperature

            </label>

            <input

                type="range"

                min={0}

                max={2}

                step={0.1}

                value={settings.temperature}

                onChange={(e) =>

                    setSettings(prev => ({

                        ...prev,

                        temperature: Number(e.target.value),

                    }))

                }

            />

            <span>

                {settings.temperature.toFixed(1)}

            </span>

        </div>

    );

}