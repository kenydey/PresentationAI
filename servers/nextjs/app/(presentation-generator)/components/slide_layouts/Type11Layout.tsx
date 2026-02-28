import React, { useState } from 'react'
import EditableText from '../EditableText'
import { Plus } from 'lucide-react';
import ElementMenu from '../ElementMenu';
import { addInfographics, deleteInfographics, updateInfographicsChart } from '@/store/slices/presentationGeneration';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '@/store/store';

type Type11LayoutProps = {
    title: string;
    slideIndex: number;
    slideId: string;
    description?: string;
    infographics: {
        title: string;
        description: string;
        chart: {
            chart_type: string;
            value: {
                number_type: string;
                numerical: number;
                suffix: string;
            }
        }
    }[];
}

const Type11Layout = ({
    title,
    slideIndex,
    slideId,
    description,
    infographics
}: Type11LayoutProps) => {
    const dispatch = useDispatch();
    const { currentColors } = useSelector((state: RootState) => state.theme);

    // const percentageColors = ['#ff00ef', '#6453ff', '#f00000']


    const handleDeleteItem = (index: number) => {
        dispatch(deleteInfographics({
            slideIndex: slideIndex,
            itemIdx: index
        }))

    }
    const handleAddItem = () => {
        dispatch(addInfographics({
            slideIndex: slideIndex,
            item: {
                title: 'Enter Title',
                description: 'Enter Description',
                chart: {
                    chart_type: infographics[0].chart.chart_type,
                    value: {
                        percentage: 80,
                        number_type: 'percentage',
                    }
                }
            }
        }))

    }
    const updateChart = ({ slideIndex, itemIdx, chart }: { slideIndex: number, itemIdx: number, chart: any }) => {
        dispatch(updateInfographicsChart({ slideIndex, itemIdx, chart }))
    }

    return (
        <div className='slide-container px-20 shadow-lg border rounded-sm w-full max-w-[1280px] font-inter py-[86px] flex flex-col items-center justify-center max-h-[720px] aspect-video bg-white'
            data-slide-element
            data-slide-index={slideIndex}
            data-slide-id={slideId}
            data-slide-type="11"
            data-element-type="slide-container"
            data-element-id={`slide-${slideIndex}-container`}
            style={{
                fontFamily: currentColors.fontFamily || 'Inter, sans-serif'
            }}
        >
            <div className={`text-center space-y-4 ${description ? 'mb-8' : 'mb-12'} w-full`}>
                <EditableText
                    slideIndex={slideIndex}
                    elementId={`slide-${slideIndex}-title`}
                    type="title"
                    isAlingCenter={true}
                    content={title}
                />
                {description && <EditableText
                    slideIndex={slideIndex}
                    elementId={`slide-${slideIndex}-description`}
                    type="description"
                    isAlingCenter={true}
                    content={description}
                />}
            </div>
            <div
                style={{
                    gridTemplateColumns: `repeat(${infographics.length}, 1fr)`
                }}
                className={`grid grid-cols-${infographics.length} gap-8  w-full relative group `}>
                <div className="absolute -inset-[2px] border-2 border-blue-500 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                <button onClick={handleAddItem} className="absolute top-1/2 -right-4 -translate-y-1/2 p-1 rounded-md bg-white shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-gray-50 z-50">
                    <Plus className="w-4 h-4 text-gray-600" />
                </button>

                {infographics.map((item, index) => (
                    <div
                        data-slide-element
                        data-slide-index={slideIndex}
                        data-element-type="slide-box"
                        data-element-id={`slide-${slideIndex}-item-${index}-box`}
                        style={{
                            boxShadow: '0 2px 10px 0 rgba(43, 43, 43, 0.2)'
                        }}
                        key={index} className={`bg-white w-full rounded-lg py-4 px-4 slide-box flex flex-col  items-center relative ${infographics.length === 1 ? 'max-w-[420px] mx-auto' : ''}`}>
                        <ElementMenu index={index} handleDeleteItem={handleDeleteItem} />
                        <div data-slide-element
                            data-slide-index={slideIndex}
                            data-element-type="filledbox"
                            data-element-id={`slide-${slideIndex}-item-${index}-box`} style={{ backgroundColor: currentColors.iconBg }} className="w-40 h-40 rounded-full  flex items-center justify-center mb-6">

                            <div className="text-center text-white">
                                <p onBlur={(e) => {
                                    updateChart({
                                        slideIndex, itemIdx: index, chart: {
                                            chart_type: item.chart.chart_type,
                                            value: {
                                                number_type: item.chart.value.number_type,
                                                numerical: parseInt(e.currentTarget.innerText),
                                                suffix: item.chart.value.suffix
                                            }
                                        }
                                    })
                                }} contentEditable suppressContentEditableWarning data-slide-element data-slide-index={slideIndex} data-element-type="text" data-is-align={true} data-element-id={`slide-${slideIndex}-value-${index}`} className='text-[24px] focus-visible:outline-none leading-[40px] font-bold'>{item.chart.value.numerical}</p>
                                <p onBlur={(e) => {
                                    updateChart({
                                        slideIndex, itemIdx: index, chart: {
                                            chart_type: item.chart.chart_type,
                                            value: {
                                                number_type: item.chart.value.number_type,
                                                numerical: item.chart.value.numerical,
                                                suffix: e.currentTarget.innerText
                                            }
                                        }
                                    })
                                }} contentEditable suppressContentEditableWarning data-slide-element data-slide-index={slideIndex} data-element-type="text" data-is-align={true} data-element-id={`slide-${slideIndex}-subtitle-${index}`} className='text-[20px] focus-visible:outline-none leading-[24px] font-bold'>{item.chart.value.suffix.toString().replace(/\*\*/g, '')}</p>
                            </div>

                        </div>
                        <div className="text-center space-y-4">
                            <EditableText
                                slideIndex={slideIndex}
                                elementId={`slide-${slideIndex}-heading-${index}`}
                                type="info-heading"
                                bodyIdx={index}
                                isAlingCenter={true}
                                content={item.title}
                            />
                            <EditableText
                                slideIndex={slideIndex}
                                elementId={`slide-${slideIndex}-description-${index}`}
                                type="info-description"
                                bodyIdx={index}
                                isAlingCenter={true}
                                content={item.description}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Type11Layout
