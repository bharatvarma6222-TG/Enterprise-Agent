import { create } from "zustand";

export interface WorkflowNode {
    id: string;
    status: "idle" | "running" | "completed" | "failed";
    message?: string;
}

interface WorkflowStore {
    nodes: WorkflowNode[];

    updateNode: (
        id: string,
        status: WorkflowNode["status"],
        message?: string
    ) => void;

    reset: () => void;
}

const initialNodes: WorkflowNode[] = [
    { id: "planner", status: "idle" },
    { id: "memory", status: "idle" },
    { id: "retrieval", status: "idle" },
    { id: "research", status: "idle" },
    { id: "critic", status: "idle" },
    { id: "writer", status: "idle" },
    { id: "evaluation", status: "idle" },
];

export const useWorkflowStore = create<WorkflowStore>((set) => ({
    nodes: initialNodes,

    updateNode: (id, status, message) =>
        set((state) => ({
            nodes: state.nodes.map((node) =>
                node.id === id
                    ? { ...node, status, message }
                    : node
            ),
        })),

    reset: () =>
        set({
            nodes: initialNodes.map((node) => ({
                ...node,
                status: "idle",
                message: undefined,
            })),
        }),
}));