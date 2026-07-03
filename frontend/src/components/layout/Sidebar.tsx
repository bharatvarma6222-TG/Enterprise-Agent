import { useChatStore } from "../../store/chatStore";

export default function Sidebar() {

    const {

        conversations,
        loadConversation,
        newChat,

    } = useChatStore();

    return (

        <div className="sidebar">

            <button onClick={newChat}>
                + New Chat
            </button>

            <div className="conversation-list">

                {conversations.map(chat => (

                    <div

                        key={chat.id}

                        className="conversation-item"

                        onClick={() => loadConversation(chat.id)}

                    >

                        💬 {chat.title}

                    </div>

                ))}

            </div>

        </div>

    );

}