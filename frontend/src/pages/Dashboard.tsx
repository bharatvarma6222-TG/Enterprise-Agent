

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";
import RightPanel from "../components/chat/RightPanel";

import PdfUpload from "../components/upload/PdfUpload";

import PlaygroundSidebar from "../components/playground/PlaygroundSidebar";
import { useChatStore } from "../store/chatStore";


import { useWorkflowStore } from "../store/workflowStore";


export default function Dashboard() {

    const updateNode = useWorkflowStore(
        state => state.updateNode
    );

    const {

        sessionId,

        setSessionId,

        messages,

        addMessage,

        updateLastAssistant,

        saveConversation,

    } = useChatStore();

    async function sendMessage(text: string) {

        addMessage({
            role: "user",
            content: text,
        });

        addMessage({
            role: "assistant",
            content: "",
        });

        const response = await fetch(

            `${import.meta.env.VITE_API_URL}/chat/stream`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                },

                body: JSON.stringify({

                    query: text,

                    session_id: sessionId,

                }),

            }

        );

        if (!response.body) return;

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        let buffer = "";

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            buffer += decoder.decode(value);

            const events = buffer.split("\n\n");

            buffer = events.pop() || "";

            for (const event of events) {

                const dataLine = event

                    .split("\n")

                    .find(line => line.startsWith("data:"));

                if (!dataLine) continue;

                const payload = JSON.parse(

                    dataLine.replace("data:", "").trim()

                );

                console.log(payload);

                switch (payload.type) {

                    case "planner_started":
                        updateNode("planner", "running");
                        break;

                    case "planner_finished":
                        updateNode("planner", "completed");
                        break;

                    case "memory_started":
                        updateNode("memory", "running");
                        break;

                    case "memory_finished":
                        updateNode("memory", "completed");
                        break;

                    case "retrieval_started":
                        updateNode("retrieval", "running");
                        break;

                    case "retrieval_finished":
                        updateNode("retrieval", "completed");
                        break;

                    case "research_started":
                        updateNode("research", "running");
                        break;

                    case "research_finished":
                        updateNode("research", "completed");
                        break;

                    case "critic_started":
                        updateNode("critic", "running");
                        break;

                    case "critic_finished":
                        updateNode("critic", "completed");
                        break;

                    case "writer_started":
                        console.log("messages length =", messages.length);
                        console.log(messages);
                        updateNode("writer", "running");
                        break;

                    case "token": {

                        updateLastAssistant(
                            payload.data.token,
                            true
                        );

                        break;
                    }

                    case "writer_finished": {

                        updateNode("writer", "completed");

                        saveConversation();

                        break;
                    }

                    case "evaluation_started":
                        updateNode("evaluation", "running");
                        break;

                    case "evaluation_finished":
                        updateNode("evaluation", "completed");
                        break;

                }

            }

        }

    }

    return (

        <div className="h-screen flex flex-col bg-zinc-950 text-white">

            <Header />

            <div className="flex flex-1 overflow-hidden">

                <Sidebar />

                <div className="flex flex-col flex-1">

                    <PdfUpload
                        onUploaded={(id) => {

                            console.log("SESSION:", id);

                            setSessionId(id);

                        }}
                    />

                    <ChatWindow

                        messages={messages}

                    />

                    <ChatInput

                        onSend={sendMessage}

                    />

                </div>

                <RightPanel />

                <PlaygroundSidebar />

            </div>

        </div>

    );

}