import cv2
import json
import numpy as np
import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("▼ DetectSudokuFrame")

    src = req.params.get("img")
    if not src:
        try:
            req_body = req.get_body()
        except ValueError as ex:
            logging.error(f"ValueError!!: {str(ex)}")
        else:
            src = req_body
    
    if src:
        # ファイル読込
        _bytes = np.frombuffer(req_body, np.uint8)
        img = cv2.imdecode(_bytes, cv2.IMREAD_GRAYSCALE)

        # Canny
        edges = cv2.Canny(img, 100, 200, apertureSize=3)
        
        # 膨張処理
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        edges = cv2.dilate(edges, kernel)
        
        # フレーム検出
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # 面積でフィルタリング
        rects = []
        for cnt, hrchy in zip(contours, hierarchy[0]):
            # 面積が小さいものは除く
            if cv2.contourArea(cnt) < 500:
                continue
            # ルートノードは除く
            if hrchy[3] == -1:
                continue
            # 輪郭を囲む長方形を計算する
            rect = cv2.minAreaRect(cnt)
            rect_points = cv2.boxPoints(rect).astype(int)
            rects.append(rect_points)

        # x-y順でソート
        rects = sorted(rects, key=lambda x: (x[0][1], x[0][0]))

        ret_dict = {}
        if rects:
            for i in range(0, len(rects)):
                ret_dict[f"num{i}"] = {}
                ret_sub_dict = {}
                for pos in range(0, 4):
                    ret_sub_dict[f"pos{pos}"] = {}
                    ret_sub_sub_dict = {}
                    for axis in range(0, 2):
                        str_axis = "x" if axis == 0 else "y"
                        ret_sub_sub_dict[str_axis] = int(rects[i][pos][axis])
                    ret_sub_dict[f"pos{pos}"] = ret_sub_sub_dict
                ret_dict[f"num{i}"] = ret_sub_dict


        logging.info("▲ DetectSudokuFrame")
        return func.HttpResponse(json.dumps(ret_dict), status_code=200)

    else:
        return func.HttpResponse("Parameter 'img' was not found.", status_code=400)
