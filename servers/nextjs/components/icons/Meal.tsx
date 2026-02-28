import { cn } from '@/lib/utils'
import React from 'react'

const MealIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M4 11a2.5 2.5 0 0 1 5 0v2a2.5 2.5 0 0 1-1.5 2.292V28.5a1 1 0 1 1-2 0V15.292A2.5 2.5 0 0 1 4 13v-2ZM27 19.5a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z" fill="currentColor" />
            <path d="M20 29.5c5.523 0 10-4.477 10-10s-4.477-10-10-10-10 4.477-10 10 4.477 10 10 10Zm8-10a8 8 0 1 1-16 0 8 8 0 0 1 16 0ZM34.5 15.292A2.5 2.5 0 0 0 36 13v-2c0-.459-.123-.888-.339-1.258C35.453 9.386 35 9.588 35 10v2a.5.5 0 0 1-1 0v-2a.5.5 0 0 0-1 0v2a.5.5 0 0 1-1 0v-1.999c0-.412-.454-.614-.661-.258-.216.37-.339.799-.339 1.257v2a2.5 2.5 0 0 0 1.5 2.292V28.5a1 1 0 1 0 2 0V15.292Z" fill="currentColor" />
        </svg>
    )
}

export default MealIcon 