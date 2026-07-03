import { useRef } from "react";

interface Props {
    onUploaded: (sessionId: string) => void;
}

export default function PdfUpload({ onUploaded }: Props) {

    const inputRef = useRef<HTMLInputElement>(null);

    async function upload(file: File) {

        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch(
            `${import.meta.env.VITE_API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        console.log(data);

        onUploaded(data.session_id);

        alert("Uploaded successfully");
    }

    return (
        <div className="p-4">

            <button
                onClick={() => inputRef.current?.click()}
                className="bg-green-600 px-4 py-2 rounded"
            >
                Upload PDF
            </button>

            <input
                ref={inputRef}
                type="file"
                hidden
                accept=".pdf"
                onChange={(e) => {

                    const file = e.target.files?.[0];

                    if (file)
                        upload(file);

                }}
            />

        </div>
    );
}