from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from services import csv_parser,get_insights,visualizer,ppt_generator,chart_recommander
from utils import file_upload
import os

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    csv_path = file_upload.save_temp_file(file)
    structurd_csv,df = csv_parser.process_clean_csv(csv_path)
    summary = get_insights.generate_summary(structurd_csv)
    insights_list = get_insights.extract_insights(structurd_csv)
    specs = chart_recommander.recommend_charts(df)
    charts = visualizer.generate_charts(df,specs)
    ppt_path = ppt_generator.create_ppt(summary, insights_list, charts)

    if not os.path.exists(ppt_path):
        raise HTTPException(500, "Could not generate PPT")
    # FileResponse will set appropriate headers:
    return FileResponse(
        path=ppt_path,
        filename=os.path.basename(ppt_path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    