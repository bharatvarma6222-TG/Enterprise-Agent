import { useWorkflowStore } from "../../store/workflowStore";

const statusColor = {
    idle: "bg-zinc-600",
    running: "bg-yellow-500 animate-pulse",
    completed: "bg-green-500",
    failed: "bg-red-500",
};

const statusText = {
    idle: "Waiting",
    running: "Running...",
    completed: "Completed",
    failed: "Failed",
};

export default function RightPanel() {

    const nodes = useWorkflowStore((state) => state.nodes);

    return (

        <div className="w-80 border-l border-zinc-800 bg-zinc-900 flex flex-col">

            <div className="p-4 border-b border-zinc-800">

                <h2 className="text-lg font-semibold">

                    Workflow

                </h2>

                <p className="text-xs text-zinc-400 mt-1">

                    LangGraph Execution

                </p>

            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-3">

                {nodes.map((node) => (

                    <div
                        key={node.id}
                        className="flex items-center justify-between rounded-lg border border-zinc-700 p-3 bg-zinc-800"
                    >

                        <div>

                            <div className="font-medium capitalize">

                                {node.id}

                            </div>

                            <div className="text-xs text-zinc-400">

                                {statusText[node.status]}

                            </div>

                        </div>

                        <div
                            className={`h-3 w-3 rounded-full ${statusColor[node.status]}`}
                        />

                    </div>

                ))}

            </div>

        </div>

    );

}