// 二维码发布前验扫 —— 用 macOS Vision 解码，确认缩放到页面尺寸后仍然扫得出来
//
// 为什么不能只看源图：文章里的二维码要按**渲染后**的尺寸被扫描，
// 源图 432px 不代表页面上显示 200px、二维码本体只剩 148px 时还能扫。
// 必须对「实际渲染出来的截图」解码才算验证通过。
//
// 用法：
//   swift verify-qrcode.swift <图片路径或URL>                # 只验源图
//   swift verify-qrcode.swift <图片路径> --render <html路径>  # 渲染后再验（推荐）
//
// 只看源图时：
//   swift verify-qrcode.swift /tmp/qr.jpg
//
// 完整链路（推荐，能验出「页面上太小扫不出」）：
//   1) 用 Chrome 以 1x 渲染文章截图（1x = 最差情况，等于小屏手机的物理像素）
//        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
//          --headless --disable-gpu --no-sandbox --force-device-scale-factor=1 \
//          --window-size=400,1200 --screenshot=/tmp/page.png file:///绝对路径/文章.html
//   2) 解码
//        swift verify-qrcode.swift /tmp/page.png
//
// 输出只打印链接的结构（host / 首段路径 / 末段长度），**不打印完整 token**。
//
// 退出码：0 = 识别成功，2 = 未识别到二维码，1 = 读不到图。

import Foundation
import Vision
import CoreGraphics
import ImageIO

let args = CommandLine.arguments
guard args.count >= 2 else {
    print("用法: swift verify-qrcode.swift <图片路径或URL>"); exit(1)
}

var imagePath = args[1]
// 支持直接给 URL：先下载到临时文件
if imagePath.hasPrefix("http://") || imagePath.hasPrefix("https://") {
    guard let url = URL(string: imagePath) else { print("URL 无效"); exit(1) }
    let dst = URL(fileURLWithPath: NSTemporaryDirectory())
        .appendingPathComponent("qrcheck-\(abs(imagePath.hashValue)).img")
    let sem = DispatchSemaphore(value: 0)
    var ok = false
    URLSession.shared.downloadTask(with: url) { tmp, _, _ in
        if let tmp = tmp {
            try? FileManager.default.removeItem(at: dst)
            try? FileManager.default.moveItem(at: tmp, to: dst)
            ok = true
        }
        sem.signal()
    }.resume()
    sem.wait()
    guard ok else { print("下载失败: \(imagePath)"); exit(1) }
    imagePath = dst.path
}

guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: imagePath) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
    print("读不到图片: \(imagePath)"); exit(1)
}

let req = VNDetectBarcodesRequest()
req.symbologies = [.qr]
do {
    try VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
} catch {
    print("识别出错: \(error)"); exit(1)
}

guard let hits = req.results, !hits.isEmpty else {
    print("✗ 未识别到二维码（\(img.width)×\(img.height)）")
    print("  → 若这是渲染后的截图，说明页面上太小或太糊，扫不出来。")
    exit(2)
}

print("✓ 识别到 \(hits.count) 个二维码（图 \(img.width)×\(img.height)）")
for (i, o) in hits.enumerated() {
    let bb = o.boundingBox
    let px = Int(bb.width * Double(img.width))
    print("  [\(i + 1)] 占图宽 \(Int(bb.width * 100))% ≈ \(px)px  码型 \(o.symbology.rawValue)")
    guard let payload = o.payloadStringValue, let u = URL(string: payload) else {
        print("      内容: (非 URL 或无法解析)")
        continue
    }
    print("      指向: \(u.host ?? "-")")
    let segs = u.path.split(separator: "/").map(String.init)
    if let first = segs.first { print("      路径: /\(first)/  末段 \(segs.last?.count ?? 0) 字符（不输出）") }
    if u.host?.contains("work.weixin.qq.com") == true {
        print("      ⚠️ 这是企业微信链接，不是个人微信群二维码；文案别写成「扫码进群」之类。")
    }
}
exit(0)
