import type { Dispatch, SetStateAction } from "react";
import type { LLMSettings } from "../../hooks/useLLMSettings";

interface Props {
    settings: LLMSettings;
    setSettings: Dispatch<SetStateAction<LLMSettings>>;
}

const providers = [
    "groq",
    "openai",
    "gemini",
    "ollama",
];

export default function ProviderSelector({

    settings,

    setSettings,

}: Props) {

    function handleChange(
        e: React.ChangeEvent<HTMLSelectElement>
    ) {

        setSettings(prev => ({

            ...prev,

            provider: e.target.value,

            model: "",

        }));

    }

    return (

        <div className="playground-field">

            <label>

                Provider

            </label>

            <select

                value={settings.provider}

                onChange={handleChange}

            >

                {

                    providers.map(provider => (

                        <option

                            key={provider}

                            value={provider}

                        >

                            {provider.toUpperCase()}

                        </option>

                    ))

                }

            </select>

        </div>

    );

}