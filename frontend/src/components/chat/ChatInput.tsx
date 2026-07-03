import { useState } from "react";

interface Props {

    onSend: (text: string) => void;

}

export default function ChatInput({

    onSend

}: Props) {

    const [text, setText] = useState("");

    function send() {

        if (!text.trim()) return;

        onSend(text);

        setText("");

    }

    return (

        <div className="border-t border-zinc-800 p-4 flex gap-3">

            <input

                className="flex-1 rounded-lg bg-zinc-800 p-3 outline-none"

                value={text}

                onChange={(e) =>

                    setText(e.target.value)

                }

                onKeyDown={(e) => {

                    if (e.key === "Enter")

                        send();

                }}

                placeholder="Ask anything..."

            />

            <button

                onClick={send}

                className="bg-blue-600 px-5 rounded-lg"

            >

                Send

            </button>

        </div>

    );

}