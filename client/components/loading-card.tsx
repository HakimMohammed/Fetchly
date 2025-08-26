import React from 'react';

interface LoadingCardProps {
    text: string;
    className?: string;
}

const LoadingCard: React.FC<LoadingCardProps> = ({ text, className = '' }) => {
    return (
        <div className="fixed inset-0 flex items-center justify-center z-50">
            <div className="absolute inset-0 bg-background/80 backdrop-blur-xs"></div>

            <div className={`
        relative 
        w-64 h-64 
        bg-background/80 
        backdrop-blur-md 
        border border-border 
        rounded-lg 
        shadow-lg 
        flex items-center justify-center 
        p-6
        ${className}
      `}>
                <div className="flex flex-col items-center justify-center space-y-4">
                    <div className="w-12 h-12 border-4 border-muted border-t-primary rounded-full animate-spin"></div>
                    <p className="text-card-foreground text-center font-medium text-lg">{text}</p>
                </div>
            </div>
        </div>
    );
};

export default LoadingCard;