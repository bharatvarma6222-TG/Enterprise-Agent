
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
    // ============================================================
    // WORKFLOW STORE
    // ============================================================

    const updateNode = useWorkflowStore(
        (state) => state.updateNode
    );

    // ============================================================
    // CHAT STORE
    // ============================================================

    const {
        sessionId,
        setSessionId,
        messages,
        addMessage,
        updateLastAssistant,
        saveConversation,
    } = useChatStore();

    // ============================================================
    // SEND MESSAGE
    // ============================================================

    async function sendMessage(text: string) {
        try {
            // ----------------------------------------------------
            // ADD USER MESSAGE
            // ----------------------------------------------------

            addMessage({
                role: "user",
                content: text,
            });

            // ----------------------------------------------------
            // ADD EMPTY ASSISTANT MESSAGE
            // ----------------------------------------------------

            addMessage({
                role: "assistant",
                content: "",
            });

            console.log(
                "SENDING MESSAGE:",
                text
            );

            console.log(
                "SESSION ID:",
                sessionId
            );

            // ----------------------------------------------------
            // CONNECT TO STREAM
            // ----------------------------------------------------

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/chat/stream`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        Accept: "text/event-stream",
                    },

                    body: JSON.stringify({
                        query: text,
                        session_id: sessionId,
                    }),
                }
            );

            // ----------------------------------------------------
            // CHECK HTTP RESPONSE
            // ----------------------------------------------------

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}: ${response.statusText}`
                );
            }

            if (!response.body) {
                throw new Error(
                    "Streaming response body is empty"
                );
            }

            console.log(
                "STREAM CONNECTED"
            );

            // ----------------------------------------------------
            // CREATE STREAM READER
            // ----------------------------------------------------

            const reader =
                response.body.getReader();

            const decoder =
                new TextDecoder("utf-8");

            let buffer = "";

            // ====================================================
            // READ STREAM
            // ====================================================

            while (true) {
                const {
                    done,
                    value,
                } = await reader.read();

                // ------------------------------------------------
                // STREAM CLOSED
                // ------------------------------------------------

                if (done) {
                    console.log(
                        "STREAM READER FINISHED"
                    );

                    break;
                }

                // ------------------------------------------------
                // DECODE CHUNK
                // ------------------------------------------------

                buffer += decoder.decode(
                    value,
                    {
                        stream: true,
                    }
                );

                // ------------------------------------------------
                // SSE EVENTS ARE SEPARATED BY:
                //
                // \n\n
                // ------------------------------------------------

                const events =
                    buffer.split("\n\n");

                // Last event might be incomplete
                buffer =
                    events.pop() || "";

                // =================================================
                // PROCESS EVENTS
                // =================================================

                for (const event of events) {
                    if (!event.trim()) {
                        continue;
                    }

                    // ------------------------------------------------
                    // FIND DATA LINE
                    // ------------------------------------------------

                    const dataLine =
                        event
                            .split("\n")
                            .find(
                                (line) =>
                                    line.startsWith(
                                        "data:"
                                    )
                            );

                    if (!dataLine) {
                        continue;
                    }

                    // ------------------------------------------------
                    // REMOVE "data:"
                    // ------------------------------------------------

                    const rawData =
                        dataLine
                            .replace(
                                /^data:\s*/,
                                ""
                            )
                            .trim();

                    if (!rawData) {
                        continue;
                    }

                    // ------------------------------------------------
                    // PARSE JSON
                    // ------------------------------------------------

                    let payload: any;

                    try {
                        payload =
                            JSON.parse(
                                rawData
                            );
                    } catch (error) {
                        console.error(
                            "INVALID SSE JSON:",
                            rawData,
                            error
                        );

                        continue;
                    }

                    console.log(
                        "SSE PAYLOAD:",
                        payload
                    );

                    // ------------------------------------------------
                    // GET EVENT TYPE
                    // ------------------------------------------------

                    const type =
                        payload?.type ??
                        payload?.event ??
                        "";

                    console.log(
                        "SSE EVENT TYPE:",
                        type
                    );

                    // =================================================
                    // WORKFLOW EVENTS
                    // =================================================

                    switch (type) {

                        // =============================================
                        // PLANNER
                        // =============================================

                        case "planner_started":

                            console.log(
                                "PLANNER STARTED"
                            );

                            updateNode(
                                "planner",
                                "running"
                            );

                            break;

                        case "planner_finished":

                            console.log(
                                "PLANNER FINISHED"
                            );

                            updateNode(
                                "planner",
                                "completed"
                            );

                            break;

                        // =============================================
                        // MEMORY
                        // =============================================

                        case "memory_started":

                            console.log(
                                "MEMORY STARTED"
                            );

                            updateNode(
                                "memory",
                                "running"
                            );

                            break;

                        case "memory_finished":

                            console.log(
                                "MEMORY FINISHED"
                            );

                            updateNode(
                                "memory",
                                "completed"
                            );

                            break;

                        case "memory_saved":

                            console.log(
                                "MEMORY SAVED"
                            );

                            updateNode(
                                "memory",
                                "completed"
                            );

                            break;

                        // =============================================
                        // RETRIEVAL
                        // =============================================

                        case "retrieval_started":

                            console.log(
                                "RETRIEVAL STARTED"
                            );

                            updateNode(
                                "retrieval",
                                "running"
                            );

                            break;

                        case "retrieval_finished":

                            console.log(
                                "RETRIEVAL FINISHED"
                            );

                            updateNode(
                                "retrieval",
                                "completed"
                            );

                            break;

                        // =============================================
                        // RESEARCH
                        // =============================================

                        case "research_started":

                            console.log(
                                "RESEARCH STARTED"
                            );

                            updateNode(
                                "research",
                                "running"
                            );

                            break;

                        case "research_finished":

                            console.log(
                                "RESEARCH FINISHED"
                            );

                            updateNode(
                                "research",
                                "completed"
                            );

                            break;

                        // =============================================
                        // CRITIC
                        // =============================================

                        case "critic_started":

                            console.log(
                                "CRITIC STARTED"
                            );

                            updateNode(
                                "critic",
                                "running"
                            );

                            break;

                        case "critic_finished":

                            console.log(
                                "CRITIC FINISHED"
                            );

                            updateNode(
                                "critic",
                                "completed"
                            );

                            break;

                        // =============================================
                        // WRITER
                        // =============================================

                        case "writer_started":

                            console.log(
                                "WRITER STARTED"
                            );

                            updateNode(
                                "writer",
                                "running"
                            );

                            break;

                        case "writer_finished":

                            console.log(
                                "WRITER FINISHED"
                            );

                            updateNode(
                                "writer",
                                "completed"
                            );

                            break;

                        // =============================================
                        // EVALUATION
                        // =============================================

                        case "evaluation_started":

                            console.log(
                                "EVALUATION STARTED"
                            );

                            updateNode(
                                "evaluation",
                                "running"
                            );

                            break;

                        case "evaluation_finished":

                            console.log(
                                "EVALUATION FINISHED"
                            );

                            updateNode(
                                "evaluation",
                                "completed"
                            );

                            break;

                        // =================================================
                        // TOKEN
                        // =================================================

                        case "token": {
                            let token = "";

                            // Backend:
                            //
                            // {
                            //     "type": "token",
                            //     "data": {
                            //         "token": "Hello"
                            //     }
                            // }

                            if (
                                typeof payload?.data?.token ===
                                "string"
                            ) {
                                token =
                                    payload.data.token;
                            }

                            // Fallback
                            else if (
                                typeof payload?.token ===
                                "string"
                            ) {
                                token =
                                    payload.token;
                            }

                            // Another fallback
                            else if (
                                typeof payload?.data ===
                                "string"
                            ) {
                                token =
                                    payload.data;
                            }

                            console.log(
                                "TOKEN RECEIVED:",
                                token
                            );

                            if (
                                token.length > 0
                            ) {
                                updateLastAssistant(
                                    token,
                                    true
                                );
                            }

                            break;
                        }

                        // =================================================
                        // FINAL ANSWER
                        // =================================================

                        case "final_answer": {
                            console.log(
                                "FINAL ANSWER EVENT RECEIVED:",
                                payload
                            );

                            // ------------------------------------------------
                            // Extract final answer
                            // ------------------------------------------------

                            const answer =
                                payload?.data?.answer ??
                                payload?.answer ??
                                payload?.data ??
                                "";

                            console.log(
                                "FINAL ANSWER TEXT:",
                                answer
                            );

                            // ------------------------------------------------
                            // Update assistant message
                            // ------------------------------------------------

                            if (
                                typeof answer ===
                                    "string" &&
                                answer.length > 0
                            ) {
                                updateLastAssistant(
                                    answer,
                                    false
                                );
                            }

                            break;
                        }

                        // =================================================
                        // GUARDRAILS
                        // =================================================

                        case "guardrail_started":

                            console.log(
                                "GUARDRAIL STARTED"
                            );

                            break;

                        case "guardrail_finished":

                            console.log(
                                "GUARDRAIL FINISHED"
                            );

                            break;

                        case "guardrail_blocked": {

                            console.log(
                                "GUARDRAIL BLOCKED"
                            );

                            const blockedMessage =
                                payload?.data ??
                                payload?.message ??
                                "Request blocked";

                            updateLastAssistant(
                                String(
                                    blockedMessage
                                ),
                                false
                            );

                            break;
                        }

                        // =================================================
                        // STREAM ERROR
                        // =================================================

                        case "stream_error": {

                            console.error(
                                "STREAM ERROR:",
                                payload
                            );

                            const errorMessage =
                                payload?.message ??
                                payload?.data ??
                                "Something went wrong.";

                            updateLastAssistant(
                                String(
                                    errorMessage
                                ),
                                false
                            );

                            break;
                        }

                        // =================================================
                        // STREAM FINISHED
                        // =================================================

                        case "stream_finished":

                            console.log(
                                "STREAM FINISHED EVENT RECEIVED"
                            );

                            saveConversation();

                            break;

                        // =================================================
                        // UNKNOWN
                        // =================================================

                        default:

                            console.log(
                                "UNKNOWN SSE EVENT:",
                                payload
                            );

                            break;
                    }
                }
            }

            console.log(
                "CHAT STREAM COMPLETED"
            );

        } catch (error) {

            console.error(
                "CHAT STREAM ERROR:",
                error
            );

            updateLastAssistant(
                "Sorry, something went wrong while processing your request.",
                false
            );
        }
    }

    // ============================================================
    // UI
    // ============================================================

    return (
        <div className="h-screen flex flex-col bg-zinc-950 text-white">

            <Header />

            <div className="flex flex-1 overflow-hidden">

                <Sidebar />

                <div className="flex flex-col flex-1">

                    <PdfUpload
                        onUploaded={(id) => {

                            console.log(
                                "PDF SESSION ID:",
                                id
                            );

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

