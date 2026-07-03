import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

export interface Conversation {
    id: string;
    title: string;
    messages: ChatMessage[];
    createdAt: number;
}

interface ChatStore {

    sessionId: string;

    messages: ChatMessage[];

    conversations: Conversation[];

    setSessionId: (id: string) => void;

    setMessages: (messages: ChatMessage[]) => void;

    addMessage: (message: ChatMessage) => void;

    updateLastAssistant: (
        content: string,
        append?: boolean
    ) => void;

    newChat: () => void;

    saveConversation: () => void;

    loadConversation: (id: string) => void;

}

export const useChatStore = create<ChatStore>()(

    persist(

        (set, get) => ({

            sessionId: crypto.randomUUID(),

            messages: [],

            conversations: [],

            setSessionId: (id) =>
                set({
                    sessionId: id
                }),

            setMessages: (messages) =>
                set({
                    messages
                }),

            addMessage: (message) =>
                set(state => ({
                    messages: [
                        ...state.messages,
                        message
                    ]
                })),

            updateLastAssistant: (
                content,
                append = false
            ) =>

                set(state => {

                    const msgs = [...state.messages];

                    for (let i = msgs.length - 1; i >= 0; i--) {

                        if (msgs[i].role === "assistant") {

                            msgs[i] = {

                                ...msgs[i],

                                content: append
                                    ? msgs[i].content + content
                                    : content,

                            };

                            break;

                        }

                    }

                    return {
                        messages: msgs
                    };

                }),

            newChat: () =>
                set({

                    sessionId: crypto.randomUUID(),

                    messages: [],

                }),

            saveConversation: () => {

                const state = get();

                if (state.messages.length === 0)
                    return;

                const firstUser = state.messages.find(
                    m => m.role === "user"
                );

                const title = firstUser
                    ? (
                        firstUser.content.length > 35
                            ? firstUser.content.slice(0, 35) + "..."
                            : firstUser.content
                    )
                    : "New Chat";

                const conversation: Conversation = {

                    id: state.sessionId,

                    title,

                    messages: [...state.messages],

                    createdAt: Date.now(),

                };

                set(prev => ({

                    conversations: [

                        conversation,

                        ...prev.conversations.filter(
                            c => c.id !== conversation.id
                        ),

                    ],

                }));

            },

            loadConversation: (id) => {

                const convo = get().conversations.find(
                    c => c.id === id
                );

                if (!convo)
                    return;

                set({

                    sessionId: convo.id,

                    messages: [...convo.messages],

                });

            },

        }),

        {

            name: "enterprise-agent-chat",

        }

    )

);