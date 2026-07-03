import client from "./client";

export async function getSettings() {
    const res = await client.get("/settings/llm");
    return res.data;
}

export async function saveSettings(data: any) {
    const res = await client.post("/settings/llm", data);
    return res.data;
}

export async function getModels(provider: string) {
    const res = await client.get(
        `/settings/models?provider=${provider}`
    );

    return res.data;
}