import { useEffect, useState } from "react";

import {
    getSettings,
    saveSettings,
    getModels,
} from "../api/settings";

export interface LLMSettings {

    provider: string;

    api_key: string;

    model: string;

    temperature: number;

    max_tokens: number;

}

export function useLLMSettings() {

    const [settings, setSettings] = useState<LLMSettings>({

        provider: "groq",

        api_key: "",

        model: "",

        temperature: 0.2,

        max_tokens: 4096,

    });

    const [models, setModels] = useState<string[]>([]);

    const [loading, setLoading] = useState(false);

    // ----------------------------
    // Load Settings
    // ----------------------------

    useEffect(() => {

        load();

    }, []);

    async function load() {

        try {

            setLoading(true);

            const data = await getSettings();

            setSettings(data);

            const availableModels = await getModels(
                data.provider
            );

            setModels(availableModels);

        }

        catch (err) {

            console.error(
                "Failed to load settings:",
                err
            );

        }

        finally {

            setLoading(false);

        }

    }

    // ----------------------------
    // Change Provider
    // ----------------------------

    async function changeProvider(

        provider: string

    ) {

        try {

            const availableModels = await getModels(
                provider
            );

            setModels(
                availableModels
            );

            setSettings(prev => ({

                ...prev,

                provider,

                model:
                    availableModels.length > 0
                        ? availableModels[0]
                        : "",

            }));

        }

        catch (err) {

            console.error(
                "Failed to load models:",
                err
            );

        }

    }

    // ----------------------------
    // Save Settings
    // ----------------------------

    async function save() {

        try {

            setLoading(true);

            await saveSettings(
                settings
            );

        }

        catch (err) {

            console.error(
                "Failed to save settings:",
                err
            );

        }

        finally {

            setLoading(false);

        }

    }

    return {

        settings,

        setSettings,

        models,

        loading,

        changeProvider,

        save,

        reload: load,

    };

}