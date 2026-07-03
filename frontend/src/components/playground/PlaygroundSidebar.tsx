import "./playground.css";

import ProviderSelector from "./ProviderSelector";
import ApiKeyInput from "./ApiKeyInput";
import ModelSelector from "./ModelSelector";
import TemperatureSlider from "./TemperatureSlider";
import MaxTokensSlider from "./MaxTokensSlider";
import SaveButton from "./SaveButton";
import CurrentModelCard from "./CurrentModelCard";

import { useLLMSettings } from "../../hooks/useLLMSettings";

export default function PlaygroundSidebar() {

    const {

        settings,

        setSettings,

        models,

        save,

    } = useLLMSettings();

    return (

        <div className="playground-sidebar">

            <h2>AI Playground</h2>

            <ProviderSelector
                settings={settings}
                setSettings={setSettings}
            />

            <ApiKeyInput
                settings={settings}
                setSettings={setSettings}
            />

            <ModelSelector
                settings={settings}
                setSettings={setSettings}
                models={models}
            />

            <TemperatureSlider
                settings={settings}
                setSettings={setSettings}
            />

            <MaxTokensSlider
                settings={settings}
                setSettings={setSettings}
            />

            <SaveButton
                save={save}
            />

            <CurrentModelCard
                settings={settings}
            />

        </div>

    );

}