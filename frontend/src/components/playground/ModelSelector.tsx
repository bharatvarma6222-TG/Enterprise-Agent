import type { Dispatch, SetStateAction } from "react";
import type { LLMSettings } from "../../hooks/useLLMSettings";

interface Props {

    settings: LLMSettings;

    setSettings: Dispatch<
        SetStateAction<LLMSettings>
    >;

    models: string[];

}

export default function ModelSelector({

    settings,

    setSettings,

    models,

}: Props) {

    function handleChange(

        e: React.ChangeEvent<HTMLSelectElement>

    ) {

        setSettings(prev => ({

            ...prev,

            model: e.target.value,

        }));

    }

    return (

        <div className="playground-field">

            <label>

                Model

            </label>

            <select

                value={settings.model}

                onChange={handleChange}

            >

                {

                    models.length === 0

                        ?

                        (

                            <option value="">

                                No Models

                            </option>

                        )

                        :

                        models.map(model => (

                            <option

                                key={model}

                                value={model}

                            >

                                {model}

                            </option>

                        ))

                }

            </select>

        </div>

    );

}