import { cn } from '@/lib/utils'
import React from 'react'

const LightBulbIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M9.098 16.38C8.224 9.826 13.324 4 19.938 4h1.019c6.613 0 11.713 5.825 10.84 12.38a13.5 13.5 0 0 1-1.661 4.914l-2.085 3.649A2.098 2.098 0 0 1 26.23 26H14.665a2.098 2.098 0 0 1-1.822-1.057l-2.085-3.649a13.5 13.5 0 0 1-1.66-4.913Zm12.145-6.317a.5.5 0 0 0-.68.194l-1.675 3.014A1.5 1.5 0 0 0 20.2 15.5h.616a.5.5 0 0 1 .44.74l-2.194 4.02a.5.5 0 1 0 .878.48l2.193-4.022a1.5 1.5 0 0 0-1.317-2.218H20.2a.5.5 0 0 1-.437-.743l1.675-3.014a.5.5 0 0 0-.194-.68ZM14.5 28a1 1 0 0 1 1-1h10a1 1 0 1 1 0 2h-10a1 1 0 0 1-1-1ZM16.5 30a1 1 0 1 0 0 2h8a1 1 0 1 0 0-2h-8ZM16.534 33a.024.024 0 0 0-.023.032l.04.122a4.162 4.162 0 0 0 7.898 0l.04-.122a.024.024 0 0 0-.023-.032h-7.933Z" fill="currentColor" />
        </svg>
    )
}

export default LightBulbIcon 