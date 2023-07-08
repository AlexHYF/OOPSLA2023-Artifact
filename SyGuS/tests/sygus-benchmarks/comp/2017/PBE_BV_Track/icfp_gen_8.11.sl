(set-logic BV)

(define-fun shr1 ((x (BitVec 64))) (BitVec 64) (bvlshr x #x0000000000000001))
(define-fun shr4 ((x (BitVec 64))) (BitVec 64) (bvlshr x #x0000000000000004))
(define-fun shr16 ((x (BitVec 64))) (BitVec 64) (bvlshr x #x0000000000000010))
(define-fun shl1 ((x (BitVec 64))) (BitVec 64) (bvshl x #x0000000000000001))
(define-fun if0 ((x (BitVec 64)) (y (BitVec 64)) (z (BitVec 64))) (BitVec 64) (ite (= x #x0000000000000001) y z))

(synth-fun f ( (x (BitVec 64))) (BitVec 64)
(

(Start (BitVec 64) (#x0000000000000000 #x0000000000000001 x (bvnot Start)
                    (shl1 Start)
 		    (shr1 Start)
		    (shr4 Start)
		    (shr16 Start)
		    (bvand Start Start)
		    (bvor Start Start)
		    (bvxor Start Start)
		    (bvadd Start Start)
		    (if0 Start Start Start)
 ))
)
)
(constraint (= (f #x11EF1BFDD6F0C041) #x008F78DFEEB78602))
(constraint (= (f #xE38F885EB968FFBD) #x071C7C42F5CB47FD))
(constraint (= (f #x78419928100802CB) #x03C20CC940804016))
(constraint (= (f #xFC4BA2FF82F2C4D3) #x07E25D17FC179626))
(constraint (= (f #x6DE412784B2CB6D5) #x036F2093C25965B6))
(constraint (= (f #x4DCF39C1F9034EB3) #x26E79CE0FC81A759))
(constraint (= (f #xB77ED1D75C4DE5E5) #x5BBF68EBAE26F2F2))
(constraint (= (f #xD767AE86034BE17B) #x6BB3D74301A5F0BD))
(constraint (= (f #xC40DFDC3ACD9AD71) #x6206FEE1D66CD6B8))
(constraint (= (f #xBABC9F900CF90063) #x5D5E4FC8067C8031))
(constraint (= (f #x803A72418DA85013) #x0000000000000000))
(constraint (= (f #x2F6300882212D189) #x0000000000000000))
(constraint (= (f #x1099CB42143C2343) #x0000000000000000))
(constraint (= (f #xA1E2580520E81707) #x0000000000000000))
(constraint (= (f #x12DE4521A0C24339) #x0000000000000000))
(constraint (= (f #x338394EECA3BB7C8) #x019C1CA77651DDBE))
(constraint (= (f #x42D832106741C0CA) #x0216C190833A0E06))
(constraint (= (f #x212EB44DCE05339E) #x010975A26E70299C))
(constraint (= (f #x1F37AA0B5A291B58) #x00F9BD505AD148DA))
(constraint (= (f #xA0D2D154639FC434) #x0506968AA31CFE21))
(constraint (= (f #x00000000000110FB) #x0000000000009105))
(constraint (= (f #x0000000000018135) #x000000000000CCA4))
(constraint (= (f #x000000000001A5C1) #x000000000000E00E))
(constraint (= (f #x0000000000018161) #x000000000000CCBB))
(constraint (= (f #x000000000001920D) #x000000000000D596))
(constraint (= (f #xD51891938F8E6FB2) #x6A8C48C9C7C737D9))
(constraint (= (f #x4DCD2A58543879E2) #x26E6952C2A1C3CF1))
(constraint (= (f #xC2DCA253604C8926) #x616E5129B0264493))
(constraint (= (f #xB3C39B53BC000E10) #x59E1CDA9DE000708))
(constraint (= (f #xB8096F1972CCE9BE) #x5C04B78CB96674DF))
(constraint (= (f #x000000000001FAAA) #x0000000000000FD5))
(constraint (= (f #x0000000000018726) #x0000000000000C39))
(constraint (= (f #x0000000000017676) #x0000000000000BB3))
(constraint (= (f #x000000000001EF86) #x0000000000000F7C))
(constraint (= (f #x0000000000010C5C) #x0000000000000862))
(constraint (= (f #x2242D19840A309EC) #x0112168CC205184F))
(constraint (= (f #x6DF345FF78E4EC8E) #x36F9A2FFBC727647))
(constraint (= (f #x8EE5D36AB0F57AFE) #x04772E9B5587ABD7))
(constraint (= (f #xDC1E97F440EFAD05) #x6E0F4BFA2077D682))
(constraint (= (f #x9E86B2C15C3932F9) #x4F435960AE1C997C))
(constraint (= (f #x14213915CC885585) #x00A109C8AE6442AC))
(constraint (= (f #x60FEA8B8B5227A3C) #x307F545C5A913D1E))
(constraint (= (f #xE2FA3614F73FA525) #x717D1B0A7B9FD292))
(constraint (= (f #x174DEE35F61683F6) #x0BA6F71AFB0B41FB))
(constraint (= (f #x26F956A9A00963D8) #x0137CAB54D004B1E))
(constraint (= (f #x00000000000144C1) #x000000000000AC86))
(constraint (= (f #x980827D680087D41) #x0000000000000000))
(constraint (= (f #x000000000001E504) #x0000000000000F28))
(constraint (= (f #x5244142A4249A0EB) #x29220A152124D075))
(constraint (= (f #x2CF300C6118AE115) #x01679806308C5708))
(constraint (= (f #x6ECD62BABDDDC7AA) #x03766B15D5EEEE3D))
(constraint (= (f #x03E17F33097BFC4B) #x01F0BF9984BDFE25))
(constraint (= (f #xE5ACCD7695EDE569) #x72D666BB4AF6F2B4))
(constraint (= (f #xF7D9C45F99AC0F9B) #x07BECE22FCCD607C))
(constraint (= (f #xC6F829024688B037) #x0000000000000000))
(constraint (= (f #x7CDC03DED468F821) #x03E6E01EF6A347C1))
(constraint (= (f #x91BA618859BA60FD) #x048DD30C42CDD307))
(constraint (= (f #xA3D72CA88FA42CF5) #x051EB965447D2167))
(constraint (= (f #xECF72B52FCF0E5BF) #x0767B95A97E7872D))
(constraint (= (f #xDCED42013E68B7C7) #x06E76A1009F345BE))
(constraint (= (f #xBC2941D373FF0840) #x05E14A0E9B9FF842))
(constraint (= (f #x58D54FF833CCC5D1) #x02C6AA7FC19E662E))
(constraint (= (f #xEC1CF292812949F0) #x0760E79494094A4F))
(constraint (= (f #x0A949D6C378443D5) #x0054A4EB61BC221E))
(constraint (= (f #x9890BC5393064B41) #x04C485E29C98325A))
(constraint (= (f #xE13B47427AEA0317) #x0709DA3A13D75018))
(constraint (= (f #x8B56E7EA11D97DA0) #x045AB73F508ECBED))
(constraint (= (f #x868C2923D01C2C43) #x0000000000000000))
(constraint (= (f #x927747B6C93CF097) #x0493BA3DB649E784))
(constraint (= (f #x8D82E2801A047383) #x046C171400D0239C))
(constraint (= (f #x93F52CD54CF4CDB1) #x049FA966AA67A66D))
(constraint (= (f #xF22500448260B877) #x07912802241305C3))
(constraint (= (f #x747B8A80444BB831) #x3A3DC5402225DC18))
(check-synth)
