import type { LLMSettings } from "../../hooks/useLLMSettings";

interface Props {

    settings: LLMSettings;

}

export default function CurrentModelCard({

    settings,

}: Props) {

    return (

        <div className="current-model-card">

            <h3>

                Current Configuration

            </h3>

            <p>

                <strong>Provider:</strong>

                {" "}

                {settings.provider}

            </p>

            <p>

                <strong>Model:</strong>

                {" "}

                {settings.model}

            </p>

            <p>

                <strong>Temperature:</strong>

                {" "}

                {settings.temperature}

            </p>

            <p>

                <strong>Max Tokens:</strong>

                {" "}

                {settings.max_tokens}

            </p>

        </div>

    );

}