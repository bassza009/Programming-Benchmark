บทที่ 1บทนำ

1.ความเป็นมาและความสำคัญของปัญหา
ในปัจจุบัน การประเมินประสิทธิภาพของภาษาโปรแกรมมีการศึกษาอย่างหลากหลาย ทว่างานวิจัยส่วนใหญ่มักมุ่งเน้นไปที่มิติเดียว เช่น การวัดความเร็วในการประมวลผลอัลกอริทึมพื้นฐาน หรือการใช้พลังงานในระดับตัวภาษาโดยตรง [1][2][6] อย่างไรก็ตาม ในการพัฒนาซอฟต์แวร์ระดับองค์กรยุคใหม่ ระบบไม่ได้ทำงานอย่างเป็นเอกเทศ แต่ต้องอยู่ภายใต้โครงสร้างพื้นฐานที่มีความซับซ้อน โดยเฉพาะการเปลี่ยนผ่านสู่สถาปัตยกรรมแบบ Cloud-Native ที่ต้องทำงานร่วมกับเทคโนโลยีคอนเทนเนอร์ (Containerization) และระบบจัดการฐานข้อมูลเชิงสัมพันธ์ (RDBMS)
แม้จะมีงานวิจัยที่เปรียบเทียบประสิทธิภาพระหว่างสถาปัตยกรรมแบบโมโนลิทิก (Monolithic Architecture) [3][5] และไมโครเซอร์วิส (Microservices Architecture) [3][5] ร่วมกับภาษาและระบบฐานข้อมูลที่หลากหลาย [4][7] แต่การศึกษาที่ผ่านมายังไม่ครอบคลุมและตอบคำถามได้อย่างชัดเจนว่า เมื่อภาษาโปรแกรมและเว็บเฟรมเวิร์กทำงานอยู่ภายในคอนเทนเนอร์ พร้อมทั้งเชื่อมต่อกับฐานข้อมูลภายใต้สภาวะโหลดสูง ประสิทธิภาพการทำงานจะลดทอนลงมากน้อยเพียงใด
ด้วยเหตุนี้ งานวิจัยนี้จึงนำเสนอการประเมินและเปรียบเทียบประสิทธิภาพเชิงลึกภายใต้สภาพแวดล้อมการทำงานที่แตกต่างกัน เพื่อเป็นแนวทางให้นักพัฒนาและสถาปนิกซอฟต์แวร์สามารถเลือกชุดเทคโนโลยี (Technology Stack) และปรับแต่งประสิทธิภาพ (Optimization) ได้อย่างเหมาะสมและคุ้มค่าที่สุดกับสภาพแวดล้อมโครงสร้างพื้นฐานที่มีอยู่
2.วัตถุประสงค์
1. เพื่อประเมินและเปรียบเทียบประสิทธิภาพการทำงานและภาระงานส่วนเกิน (Overhead) ระหว่างสถาปัตยกรรมแบบโมโนลิทิก (Monolithic Architecture) และสถาปัตยกรรมแบบไมโครเซอร์วิส (Microservices Architecture) ภายใต้สภาพแวดล้อมการทำงานแบบดั้งเดิม (Bare Metal) และแบบคอนเทนเนอร์ (Containerization) 2. เพื่อวิเคราะห์และเปรียบเทียบสมรรถนะของภาษาและเว็บเฟรมเวิร์กที่แตกต่างกัน (Python, Node.js, PHP, Go และ Java) ในการรองรับภาระงานฐานข้อมูลทั้งการอ่าน (GET) และการเขียน (POST) ภายใต้ระดับความซับซ้อนของข้อมูลที่หลากหลาย 
3. เพื่อศึกษาผลกระทบของการจัดสรรทรัพยากรและการจำลองระบบ (Virtualization / Container Overhead) ที่มีต่อเวลาในการตอบสนอง (Response Time) ปริมาณงานที่รองรับได้ (Throughput) และความเสถียรของระบบภายใต้สภาวะโหลดสูง
บทที่ 2เอกสารและงานวิจัยที่เกี่ยวข้อง

Narada Wickramage (2005): ได้นำเสนอ "A Benchmark for Web Service Frameworks" ซึ่งเป็นเกณฑ์มาตรฐานที่จำลองสถานการณ์ทางธุรกิจในโลกความเป็นจริง เพื่อใช้ประเมินและเปรียบเทียบประสิทธิภาพของโครงร่างบริการเว็บ (Web Service Frameworks) โดยเน้นวิเคราะห์ผลกระทบจาก ความซับซ้อนของข้อความ SOAP และ ขนาดของข้อมูล (Payload size) ที่มีต่อเวลาในการตอบสนองของระบบ
Prechelt Lutz (2002): ได้ทำการศึกษาเชิงประจักษ์ในหัวข้อ "An Empirical Comparison of Seven Programming Languages" โดยเปรียบเทียบประสิทธิภาพของภาษาโปรแกรมกลุ่ม Scripting และ Non-scripting ผ่านการแก้โจทย์เดียวกัน ผลการศึกษาชี้ให้เห็นว่า ความแตกต่างของทักษะระหว่างบุคคล (Inter-programmer variability) ส่งผลต่อประสิทธิภาพของซอฟต์แวร์มากกว่าความแตกต่างของตัวภาษาโปรแกรมเองในหลายกรณี
วิลาวัณย์ และคณะ (2559): ศึกษาเรื่อง "สถาปัตยกรรม Microservices กับเทคโนโลยี Containers" ในยุคเริ่มต้นของการใช้งาน Docker ในประเทศไทย พบว่าคอนเทนเนอร์สามารถแก้ไขปัญหาความขัดแย้งของส่วนประกอบซอฟต์แวร์ (Dependency Conflict) ได้อย่างมีประสิทธิภาพ แต่เริ่มมีข้อสังเกตเกี่ยวกับภาระงานส่วนเกิน (Overhead) ในการจัดการทรัพยากรเมื่อต้องรันบริการจำนวนมากบนฮาร์ดแวร์ที่จำกัด
Morabito et al. (2017): ทำการทดสอบ "Performance Evaluation of Docker Containers" โดยเปรียบเทียบกับเครื่องแม่ข่ายจำลอง (Virtual Machines) และเครื่องแม่ข่ายจริง (Bare-metal) ผลการศึกษาพบว่าดอกเกอร์ (Docker) มีประสิทธิภาพด้านหน่วยประมวลผลกลาง (CPU) และหน่วยความจำ (RAM) ใกล้เคียงกับเครื่องจริงมาก แต่มีความแตกต่างที่ชัดเจนในส่วนของ Network I/O ซึ่งเป็นจุดเริ่มต้นของการศึกษาเรื่อง Network Overhead ในระบบไมโครเซอร์วิส
Villamizar et al. (2017): ศึกษาเรื่อง "Evaluating the Monolithic and the Microservices Architecture Pattern" โดยทดสอบแอปพลิเคชันเดียวกันบนสองสถาปัตยกรรม พบว่า Monolithic ให้ค่าเวลาตอบสนอง (Response Time) ที่ดีกว่าในสภาวะปกติ แต่ Microservices มีความคุ้มค่าและเหมาะสมกว่าเมื่อต้องมีการขยายระบบ (Scaling) บนสภาพแวดล้อมคลาวด์
Amaral et al. (2018): ศึกษา "Performance Evaluation of Microservices" โดยมุ่งเน้นที่ค่าความหน่วง (Latency) ที่เกิดจากการสื่อสารผ่าน HTTP/REST และกระบวนการแปลงข้อมูล (JSON Serialization) พบว่าโสหุ้ยเหล่านี้จะทวีคูณเพิ่มขึ้นตามจำนวนชั้นของบริการที่เรียกต่อกัน (Service Chaining)
Shetty et al. (2020): ศึกษา "An Empirical Performance Evaluation of Docker Container and Bare Metal Server" พบว่าในภาระงานที่เน้นการเขียน/อ่านดิสก์อย่างหนัก คอนเทนเนอร์อาจมีประสิทธิภาพลดลงประมาณ 5-10% เมื่อเทียบกับระบบที่ไม่ผ่านชั้น Docker Engine
วรเทพ อหันตริก (2566): ศึกษา "การประเมินและเปรียบเทียบประสิทธิภาพการทำงานของอัลกอริทึมการขยายตัวอัตโนมัติ" บนแพลตฟอร์ม Docker และ Kubernetes พบว่าการบริหารจัดการทรัพยากร CPU เป็นปัจจัยสำคัญที่ตัดสินความเร็วในการตอบสนองของระบบภายใต้โหลดผู้ใช้งานสูง
Ruislan (2023): โครงการ "Web Frameworks Benchmark" บน GitHub ที่รวบรวมการทดสอบปริมาณงาน (Throughput) ของภาษา Go, Node.js, PHP และ Java พบว่า Go และ Java (ผ่าน Vert.x) มักให้ค่า Throughput สูงสุด แต่มีการใช้หน่วยความจำที่แตกต่างกันอย่างมีนัยสำคัญในสภาพแวดล้อมที่จำกัดทรัพยากร
Faried Effendy (2021): ได้ศึกษา "Performance Comparison of Web Frameworks" โดยทำการวิเคราะห์เชิงเปรียบเทียบสมรรถนะของเฟรมเวิร์กในภาษาต่างๆ (เช่น Java, Python, PHP) ภายใต้สภาวะโหลดที่แตกต่างกัน เพื่อวัดค่า Response Time และความสามารถในการรองรับคำร้องขอ (Requests per second) ซึ่งช่วยยืนยันความเหมาะสมในการเลือกเทคโนโลยีรันไทม์ให้สอดคล้องกับทรัพยากรระบบ
The-Benchmarker (2024): โครงการ "Which is the fastest web framework?" ทดสอบแบบข้ามเลเยอร์ (Cross-layer) บนคอนเทนเนอร์ร่วมกับฐานข้อมูล MySQL และ PostgreSQL พบข้อมูลที่สนับสนุนว่าประสิทธิภาพของ Database Driver ในแต่ละภาษามีผลต่อค่าความหน่วงรวมมากกว่าตัวภาษาโปรแกรมเองในงานประเภท CRUD
Lauwren et al. (2025): ศึกษา "Microservice and Monolith Performance Comparison in Transaction Application" สรุปผลว่าสถาปัตยกรรม Monolithic ยังคงให้ค่าเฉลี่ยความหน่วงที่ดีกว่าในเกือบทุกกรณี แต่ Microservices มีอัตราความสำเร็จ (Success Rate) ในการจัดการคำร้องขอที่สูงกว่าเมื่อเผชิญกับความหนาแน่นของผู้ใช้งานระดับสูง (High Load)
TechEmpower (2024): โครงการ "TechEmpower Framework Benchmarks" ซึ่งเป็นชุดทดสอบมาตรฐานระดับอุตสาหกรรม (Industry Benchmark Standard) ที่ทำการประเมินประสิทธิภาพของเว็บเฟรมเวิร์กหลายร้อยตัวร่วมกับระบบจัดการฐานข้อมูล (เช่น PostgreSQL และ MySQL) โดยครอบคลุมรูปแบบการทำงานทั้ง Single-query, Multi-queries, Database Updates และ Fortunes (การดึงข้อมูลร่วมกับการทำ Template Rendering)
ช่องว่างของงานวิจัย (Research Gap)
จากการทบทวนวรรณกรรม เอกสารวิชาการ และโครงการประเมินประสิทธิภาพที่เกี่ยวข้องข้างต้น พบว่าการศึกษาที่ผ่านมาส่วนใหญ่มักมุ่งเน้นการทดสอบแบบแยกมิติเดี่ยว (Isolated Single-dimension Testing) เช่น การเปรียบเทียบเฉพาะความเร็วของภาษาโปรแกรม หรือการประเมินความแตกต่างของรูปแบบสถาปัตยกรรมเพียงอย่างใดอย่างหนึ่ง ทำให้ยังขาดการศึกษาเชิงประจักษ์อย่างเป็นระบบในลักษณะการทดสอบแบบผสมผสานหลายมิติพร้อมกัน (Multi-factor Cross-combination Evaluation) ที่ผสานรวมปัจจัยสำคัญทั้งด้านภาษาโปรแกรม สถาปัตยกรรมระบบ สภาพแวดล้อมการทำงาน และระบบจัดการฐานข้อมูล ภายใต้ภาระงานประเภทต่าง ๆ เข้าด้วยกัน

บทที่ 3วิธีการดำเนินการวิจัย

งานวิจัยนี้ดำเนินตามระเบียบวิธีวิจัยเชิงทดลอง (Experimental Research) โดยใช้การออกแบบการทดลองแบบปัจจัยครบส่วน (Full-factorial Design) เพื่อศึกษาความสัมพันธ์และผลกระทบระหว่างสถาปัตยกรรมซอฟต์แวร์ รันไทม์ภาษาโปรแกรม และระบบฐานข้อมูล โดยมีขั้นตอนการดำเนินงานดังนี้
1.สภาพแวดล้อมที่ใช้ในการทดลอง
2.การออกแบบซอฟต์แวร์และระบบ
3.การกำหนดตัวแปรต้นและระดับการทดลอง
4.ประเภทของภาระงานที่ทดสอบ
5.ขั้นตอนการดำเนินการทดลอง
6.การวิเคราะห์ข้อมูล

อ้างอิง

[1] N. Wickramage, "A benchmark for web service frameworks," Master's thesis, Department of Computer Science, Indiana University, Bloomington, IN, USA, 2005.

[2] L. Prechelt, "An empirical comparison of seven programming languages," IEEE Computer, vol. 33, no. 10, pp. 23–29, Oct. 2000. doi: 10.1109/2.876288.

[3] วิลาวัณย์ รักประชาสรรค์ และ พรชัย มงคลนาม, "สถาปัตยกรรม Microservices กับเทคโนโลยี Containers," วารสารวิชาการพระจอมเกล้าพระนครเหนือ, ปีที่ 26, ฉบับที่ 3, หน้า 511–522, ก.ย.–ธ.ค. 2559.

[4] R. Morabito, J. Kjällman, and M. Komu, "Hypervisors vs. lightweight virtualization: A performance comparison," in Proc. IEEE Int. Conf. Cloud Eng. (IC2E), Tempe, AZ, USA, 2015, pp. 386–393. doi: 10.1109/IC2E.2015.74.

[5] M. Villamizar et al., "Evaluating the monolithic and the microservice architecture pattern to deploy web applications in the cloud," in Proc. 10th Int. Conf. High Perform. Comput. Commun. (HPCC), Bangor, UK, 2017, pp. 583–590. doi: 10.1109/HPCC/SmartCity/DSS.2016.0086.

[6] M. Amaral et al., "Performance evaluation of microservices architectures using containers," in Proc. 14th Int. Symp. Netw. Comput. Appl. (NCA), Cambridge, MA, USA, 2015, pp. 27–34. doi: 10.1109/NCA.2015.10.

[7] J. Shetty et al., "An empirical performance evaluation of Docker container and bare metal server," in Proc. Int. Conf. Emerg. Trends Inf. Technol. Eng. (ic-ETITE), Vellore, India, 2020, pp. 1–6. doi: 10.1109/ic-ETITE47903.2020.9077782.

[8] วรเทพ อหันตริก, "การประเมินและเปรียบเทียบประสิทธิภาพการทำงานของอัลกอริทึมการขยายตัวอัตโนมัติของพอดบนแพลตฟอร์มคูเบอร์เนเตส," วิทยานิพนธ์ วท.ม., คณะวิทยาการสารสนเทศ, มหาวิทยาลัยบูรพา, ชลบุรี, ประเทศไทย, 2566.

[9] R. Ruslan, "Web Frameworks Benchmark," GitHub Repository, 2023. [Online]. Available: https://github.com/the-benchmarker/web-frameworks. [Accessed: Aug. 19, 2026].

[10] F. Effendy, "Performance comparison of web frameworks based on response time and throughput," Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), vol. 5, no. 4, pp. 780–786, 2021. doi: 10.29207/resti.v5i4.3312.

[11] The-Benchmarker, "Which is the fastest web framework?," 2024. [Online]. Available: https://web-frameworks-benchmark.netlify.app/. [Accessed: Aug. 19, 2026].

[12] R. Lauwren, A. F. Wicaksono, and D. I. Sensuse, "Microservice and monolith performance comparison in transaction application," in Proc. Int. Conf. Adv. Comput. Sci. Inf. Syst. (ICACSIS), 2025, pp. 1–8.

[13] TechEmpower, "TechEmpower Web Framework Benchmarks," 2024. [Online]. Available: https://www.techempower.com/benchmarks/. [Accessed: Aug. 19, 2026].