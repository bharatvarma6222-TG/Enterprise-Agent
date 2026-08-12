import { useState } from "react";
import { useChatStore } from "../../store/chatStore";

export default function Sidebar() {
    const {
        conversations,
        sessionId,
        loadConversation,
        newChat,
        deleteConversation,
        clearAllConversations,
    } = useChatStore();

    const [hoveredChat, setHoveredChat] =
        useState<string | null>(null);

    const handleDelete = (
        event: React.MouseEvent,
        id: string
    ) => {
        event.stopPropagation();

        const confirmed = window.confirm(
            "Delete this conversation?"
        );

        if (confirmed) {
            deleteConversation(id);
        }
    };

    const handleClearAll = () => {
        if (conversations.length === 0) {
            return;
        }

        const confirmed = window.confirm(
            "Delete all conversations? This cannot be undone."
        );

        if (confirmed) {
            clearAllConversations();
        }
    };

    return (
        <aside
            style={{
                width: "260px",
                height: "100%",
                background: "#09090b",
                borderRight: "1px solid #27272a",
                display: "flex",
                flexDirection: "column",
                boxSizing: "border-box",
            }}
        >
            {/* Header */}
            <div
                style={{
                    padding: "16px 14px",
                    borderBottom: "1px solid #27272a",
                }}
            >
                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                    }}
                >
                    {/* New Chat */}
                    <button
                        onClick={newChat}
                        style={{
                            flex: 1,
                            height: "38px",
                            border: "1px solid #3f3f46",
                            borderRadius: "8px",
                            background: "#18181b",
                            color: "#f4f4f5",
                            fontSize: "14px",
                            fontWeight: 500,
                            cursor: "pointer",
                            transition:
                                "background 0.15s ease",
                        }}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.background =
                                "#27272a";
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.background =
                                "#18181b";
                        }}
                    >
                        + New Chat
                    </button>

                    {/* Clear All */}
                    <button
                        onClick={handleClearAll}
                        disabled={
                            conversations.length === 0
                        }
                        title="Clear all conversations"
                        style={{
                            height: "38px",
                            padding: "0 12px",
                            border: "1px solid #3f3f46",
                            borderRadius: "8px",
                            background:
                                conversations.length === 0
                                    ? "#18181b"
                                    : "#18181b",
                            color:
                                conversations.length === 0
                                    ? "#52525b"
                                    : "#f87171",
                            fontSize: "13px",
                            fontWeight: 500,
                            cursor:
                                conversations.length === 0
                                    ? "not-allowed"
                                    : "pointer",
                            opacity:
                                conversations.length === 0
                                    ? 0.5
                                    : 1,
                        }}
                    >
                        Clear
                    </button>
                </div>
            </div>

            {/* Conversation list */}
            <div
                style={{
                    flex: 1,
                    overflowY: "auto",
                    padding: "10px 8px",
                }}
            >
                {conversations.length === 0 ? (
                    <div
                        style={{
                            padding: "24px 12px",
                            textAlign: "center",
                            color: "#71717a",
                            fontSize: "13px",
                        }}
                    >
                        No conversations yet
                    </div>
                ) : (
                    conversations.map((chat) => {
                        const isActive =
                            chat.id === sessionId;

                        const isHovered =
                            hoveredChat === chat.id;

                        return (
                            <div
                                key={chat.id}
                                onClick={() =>
                                    loadConversation(chat.id)
                                }
                                onMouseEnter={() =>
                                    setHoveredChat(chat.id)
                                }
                                onMouseLeave={() =>
                                    setHoveredChat(null)
                                }
                                style={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "8px",
                                    width: "100%",
                                    minHeight: "42px",
                                    padding: "6px 7px",
                                    marginBottom: "4px",
                                    boxSizing: "border-box",
                                    borderRadius: "8px",
                                    background: isActive
                                        ? "#27272a"
                                        : isHovered
                                        ? "#18181b"
                                        : "transparent",
                                    border: isActive
                                        ? "1px solid #3f3f46"
                                        : "1px solid transparent",
                                    cursor: "pointer",
                                    transition:
                                        "background 0.15s ease",
                                }}
                            >
                                {/* Chat icon */}
                                <span
                                    style={{
                                        flexShrink: 0,
                                        fontSize: "14px",
                                    }}
                                >
                                    💬
                                </span>

                                {/* Chat title */}
                                <span
                                    style={{
                                        flex: 1,
                                        minWidth: 0,
                                        overflow: "hidden",
                                        textOverflow:
                                            "ellipsis",
                                        whiteSpace: "nowrap",
                                        color: isActive
                                            ? "#ffffff"
                                            : "#d4d4d8",
                                        fontSize: "14px",
                                    }}
                                    title={chat.title}
                                >
                                    {chat.title}
                                </span>

                                {/* Delete button */}
                                {isHovered && (
                                    <button
                                        onClick={(event) =>
                                            handleDelete(
                                                event,
                                                chat.id
                                            )
                                        }
                                        title="Delete conversation"
                                        style={{
                                            flexShrink: 0,
                                            width: "30px",
                                            height: "30px",
                                            display: "flex",
                                            alignItems:
                                                "center",
                                            justifyContent:
                                                "center",
                                            border: "1px solid #3f3f46",
                                            borderRadius: "6px",
                                            background:
                                                "#18181b",
                                            color: "#a1a1aa",
                                            cursor: "pointer",
                                            fontSize: "14px",
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.background =
                                                "#3f1818";
                                            e.currentTarget.style.borderColor =
                                                "#7f1d1d";
                                            e.currentTarget.style.color =
                                                "#f87171";
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.background =
                                                "#18181b";
                                            e.currentTarget.style.borderColor =
                                                "#3f3f46";
                                            e.currentTarget.style.color =
                                                "#a1a1aa";
                                        }}
                                    >
                                        🗑
                                    </button>
                                )}
                            </div>
                        );
                    })
                )}
            </div>
        </aside>
    );
}