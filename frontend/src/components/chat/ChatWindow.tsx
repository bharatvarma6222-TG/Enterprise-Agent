import { useEffect, useRef } from "react";

import type { ChatMessage } from "../../store/chatStore";

interface Props {

    messages: ChatMessage[];

}

export default function ChatWindow({

    messages,

}: Props) {

    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({

            behavior: "smooth",

        });

    }, [messages]);

    return (

        <div className="flex-1 overflow-auto p-8 space-y-6">

            {

                messages.map((message, index) => (

                    <div

                        key={index}

                        className={
                            message.role === "user"
                                ? "flex justify-end"
                                : "flex justify-start"
                        }

                    >

                        <div

                            className={

                                message.role === "user"

                                    ? "bg-blue-600 text-white px-4 py-3 rounded-xl max-w-3xl whitespace-pre-wrap"

                                    : "bg-zinc-800 text-white px-4 py-3 rounded-xl max-w-4xl whitespace-pre-wrap"

                            }

                        >

                            {message.content}

                        </div>

                    </div>

                ))

            }

            <div ref={bottomRef} />

        </div>

    );

}