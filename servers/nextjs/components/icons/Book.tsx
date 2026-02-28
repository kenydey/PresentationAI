import { cn } from '@/lib/utils'
import React from 'react'

const BookIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M15 6h4v6.132l-1.168-.78a1.5 1.5 0 0 0-1.664 0l-1.168.78V6Z" fill="currentColor" />
            <path d="M20 13.066V6h8a2 2 0 0 1 2 2v18.38c0 .197-.06.389-.16.558A5.972 5.972 0 0 0 29 30c0 1.17.335 2.262.914 3.185a.524.524 0 0 1-.438.815H14a4 4 0 0 1-4-4V10a4 4 0 0 1 4-4v7.066a.5.5 0 0 0 .777.416l1.946-1.297a.5.5 0 0 1 .554 0l1.946 1.297a.5.5 0 0 0 .777-.416ZM27.148 28H13.5a2 2 0 1 0 0 4h13.648c.306 0 .53-.287.476-.589a.492.492 0 0 0-.476-.411H13.5a1 1 0 1 1 0-2h13.648a.492.492 0 0 0 .476-.411.495.495 0 0 0-.476-.589Z" fill="currentColor" />
        </svg>
    )
}

export default BookIcon 