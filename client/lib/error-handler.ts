import { toast } from "@/components/ui/use-toast";

export class AppError extends Error {
    constructor(message: string, public code?: string, public statusCode?: number) {
        super(message);
        this.name = "AppError";
    }
}

export const handleError = (error: unknown, fallbackMessage = "An unexpected error occurred") => {
    console.error("Error:", error);

    if (error instanceof AppError) {
        toast({
            title: "Error",
            description: error.message,
            variant: "destructive",
        });
        return;
    }

    if (error instanceof Error) {
        toast({
            title: "Error",
            description: error.message,
            variant: "destructive",
        });
        return;
    }

    toast({
        title: "Error",
        description: fallbackMessage,
        variant: "destructive",
    });
};

export const isNetworkError = (error: unknown): boolean => {
    return error instanceof Error && error.message.includes("Network Error");
};
