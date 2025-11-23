"use client";
import React from "react";


export default function CalendarLegend() {
return (
<div className="legend-container">
<h3>Task Legend</h3>
<ul className="legend-list">
<li><span className="legend-dot" style={{ background: '#F4C2C2' }}></span> Assignment</li>
<li><span className="legend-dot" style={{ background: '#F3E5AB' }}></span> Project</li>
<li><span className="legend-dot" style={{ background: '#AFEEEE' }}></span> Written Exam</li>
<li><span className="legend-dot" style={{ background: '#98FB98' }}></span> Practical Exam</li>
</ul>
</div>
);
}