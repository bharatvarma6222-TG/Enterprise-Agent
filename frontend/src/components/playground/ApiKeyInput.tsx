import type { Dispatch, SetStateAction } from "react";
import type { LLMSettings } from "../../hooks/useLLMSettings";

interface Props {

    settings: LLMSettings;

    setSettings: Dispatch<
        SetStateAction<LLMSettings>
    >;

}

export default function ApiKeyInput({

    settings,

    setSettings,

}: Props) {

    return (

        <div className="playground-field">

            <label>

                API Key

            </label>

            <input

                type="password"

                placeholder="Enter API Key"

                value={settings.api_key}

                onChange={(e) =>

                    setSettings(prev => ({

                        ...prev,

                        api_key: e.target.value,

                    }))

                }

            />

        </div>

    );

}