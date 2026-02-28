import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Slide } from '../../types/slide';
<<<<<<< HEAD
import { useRef } from 'react';
=======
import { useState } from 'react';
>>>>>>> 78e1006 (Initial: presenton)

interface SortableListItemProps {
    slide: Slide;
    index: number;
    selectedSlide: number;
<<<<<<< HEAD
    onSlideClick: (index: any) => void;
}

export function SortableListItem({ slide, index, selectedSlide, onSlideClick }: SortableListItemProps) {
    const lastClickTime = useRef(0);
=======
    onSlideClick: (index: number) => void;
}

export function SortableListItem({ slide, index, selectedSlide, onSlideClick }: SortableListItemProps) {
    const [mouseDownTime, setMouseDownTime] = useState(0);
>>>>>>> 78e1006 (Initial: presenton)

    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id: slide.id! });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1
    };

<<<<<<< HEAD
    const handleClick = (e: React.MouseEvent) => {
        const now = Date.now();

        // Debounce clicks - only allow one click every 300ms
        if (now - lastClickTime.current < 300) {
            return;
        }

        // Only trigger click if not dragging
        if (!isDragging) {
            lastClickTime.current = now;
=======
    const handleMouseDown = () => {
        setMouseDownTime(Date.now());
    };

    const handleMouseUp = () => {
        const mouseUpTime = Date.now();
        const timeDiff = mouseUpTime - mouseDownTime;

        // If the mouse was down for less than 200ms, consider it a click
        if (timeDiff < 200 && !isDragging) {
>>>>>>> 78e1006 (Initial: presenton)
            onSlideClick(slide.index);
        }
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
<<<<<<< HEAD
            onClick={handleClick}
            className={`p-3 cursor-pointer ring-0 border-[3px] rounded-lg slide-box
                ${selectedSlide === index
                    ? ' border-[#5141e5] '
                    : 'hover:slide-box/40 border-gray-300'
                }`}
        >
            <span className="font-medium slide-title">Slide {index + 1}</span>
          
=======
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            className={`p-3 cursor-pointer rounded-lg slide-box
                ${selectedSlide === index
                    ? 'ring-2 ring-[#5141e5] text-white'
                    : 'hover:slide-box/40'
                }`}
        >
            <span className="font-medium slide-title">Slide {index + 1}</span>
            <p className="text-sm slide-description">
                {slide.content.title}
            </p>
>>>>>>> 78e1006 (Initial: presenton)
        </div>
    );
} 