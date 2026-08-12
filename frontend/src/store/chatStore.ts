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

    deleteConversation: (id: string) => void;
    clearAllConversations: () => void;
}

export const useChatStore = create<ChatStore>()(
    persist(
        (set, get) => ({
            sessionId: crypto.randomUUID(),

            messages: [],

            conversations: [],

            setSessionId: (id) => {
                set({
                    sessionId: id,
                });
            },

            setMessages: (messages) => {
                set({
                    messages,
                });
            },

            addMessage: (message) => {
                set((state) => ({
                    messages: [
                        ...state.messages,
                        message,
                    ],
                }));
            },

            updateLastAssistant: (
                content,
                append = false
            ) => {
                set((state) => {
                    const messages = [
                        ...state.messages,
                    ];

                    for (
                        let i = messages.length - 1;
                        i >= 0;
                        i--
                    ) {
                        if (
                            messages[i].role ===
                            "assistant"
                        ) {
                            messages[i] = {
                                ...messages[i],
                                content: append
                                    ? messages[i].content +
                                      content
                                    : content,
                            };

                            break;
                        }
                    }

                    return {
                        messages,
                    };
                });
            },

            newChat: () => {
                const state = get();

                if (state.messages.length > 0) {
                    const firstUserMessage =
                        state.messages.find(
                            (message) =>
                                message.role === "user"
                        );

                    const title = firstUserMessage
                        ? firstUserMessage.content.length >
                          35
                            ? firstUserMessage.content.slice(
                                  0,
                                  35
                              ) + "..."
                            : firstUserMessage.content
                        : "New Chat";

                    const conversation: Conversation = {
                        id: state.sessionId,
                        title,
                        messages: [
                            ...state.messages,
                        ],
                        createdAt: Date.now(),
                    };

                    set((previousState) => ({
                        conversations: [
                            conversation,
                            ...previousState.conversations.filter(
                                (chat) =>
                                    chat.id !==
                                    conversation.id
                            ),
                        ],
                        sessionId:
                            crypto.randomUUID(),
                        messages: [],
                    }));

                    return;
                }

                set({
                    sessionId: crypto.randomUUID(),
                    messages: [],
                });
            },

            saveConversation: () => {
                const state = get();

                if (state.messages.length === 0) {
                    return;
                }

                const firstUserMessage =
                    state.messages.find(
                        (message) =>
                            message.role === "user"
                    );

                const title = firstUserMessage
                    ? firstUserMessage.content.length > 35
                        ? firstUserMessage.content.slice(
                              0,
                              35
                          ) + "..."
                        : firstUserMessage.content
                    : "New Chat";

                const conversation: Conversation = {
                    id: state.sessionId,
                    title,
                    messages: [
                        ...state.messages,
                    ],
                    createdAt: Date.now(),
                };

                set((previousState) => ({
                    conversations: [
                        conversation,
                        ...previousState.conversations.filter(
                            (chat) =>
                                chat.id !==
                                conversation.id
                        ),
                    ],
                }));
            },

            loadConversation: (id) => {
                const state = get();

                const conversation =
                    state.conversations.find(
                        (chat) => chat.id === id
                    );

                if (!conversation) {
                    return;
                }

                set({
                    sessionId: conversation.id,
                    messages: [
                        ...conversation.messages,
                    ],
                });
            },

            deleteConversation: (id) => {
                const state = get();

                const remainingConversations =
                    state.conversations.filter(
                        (chat) => chat.id !== id
                    );

                if (state.sessionId === id) {
                    set({
                        conversations:
                            remainingConversations,
                        sessionId:
                            crypto.randomUUID(),
                        messages: [],
                    });

                    return;
                }

                set({
                    conversations:
                        remainingConversations,
                });
            },

            clearAllConversations: () => {
                set({
                    conversations: [],
                    sessionId: crypto.randomUUID(),
                    messages: [],
                });
            },
        }),
        {
            name: "enterprise-agent-chat",
        }
    )
);