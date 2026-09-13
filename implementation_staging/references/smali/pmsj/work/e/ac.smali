.class public final Lpmsj/work/e/ac;
.super Lpmsj/work/d/c;


# instance fields
.field private final K:I

.field private final L:I

.field private final M:I

.field private final N:I

.field private final O:I

.field private final P:I

.field private final Q:I

.field private final R:I

.field private S:Lpmsj/work/d/k;

.field private T:Lpmsj/work/d/l;

.field private U:Lpmsj/work/d/l;

.field private V:Lpmsj/work/d/l;

.field private W:Lpmsj/work/d/f;

.field private X:Lpmsj/work/d/l;

.field private Y:Lpmsj/work/d/f;

.field private Z:Lpmsj/work/d/l;

.field private final a:I

.field private aa:Lpmsj/work/d/l;

.field private ab:Lpmsj/work/d/a;

.field private ac:Lpmsj/work/d/a;

.field private ad:Lpmsj/work/d/l;

.field private ae:Lpmsj/work/d/l;

.field private af:Lpmsj/work/d/l;

.field private ag:Ljava/util/Vector;

.field private ah:Lpmsj/work/d/i;

.field private ai:Z

.field private final aj:B

.field private final ak:B

.field private final al:B

.field private final am:B

.field private final an:B

.field private final ao:B

.field private final ap:B

.field private final aq:B

.field private final b:I

.field private final c:I

.field private final d:I

.field private final e:I

.field private final f:I


# direct methods
.method public constructor <init>()V
    .locals 4

    const/4 v3, 0x3

    const/4 v2, 0x1

    const/4 v1, 0x0

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const v0, 0x55b19

    iput v0, p0, Lpmsj/work/e/ac;->a:I

    const v0, 0x55b22

    iput v0, p0, Lpmsj/work/e/ac;->b:I

    const v0, 0x55b1a

    iput v0, p0, Lpmsj/work/e/ac;->c:I

    const v0, 0x55b1b

    iput v0, p0, Lpmsj/work/e/ac;->d:I

    const v0, 0x55b1c

    iput v0, p0, Lpmsj/work/e/ac;->e:I

    const v0, 0x55b1d

    iput v0, p0, Lpmsj/work/e/ac;->f:I

    const v0, 0x55b1e

    iput v0, p0, Lpmsj/work/e/ac;->K:I

    const v0, 0x55b1f

    iput v0, p0, Lpmsj/work/e/ac;->L:I

    const v0, 0x55b20

    iput v0, p0, Lpmsj/work/e/ac;->M:I

    const v0, 0x55b21

    iput v0, p0, Lpmsj/work/e/ac;->N:I

    const v0, 0x55b23

    iput v0, p0, Lpmsj/work/e/ac;->O:I

    const v0, 0x55b26

    iput v0, p0, Lpmsj/work/e/ac;->P:I

    const v0, 0x55b27

    iput v0, p0, Lpmsj/work/e/ac;->Q:I

    const v0, 0x55b28

    iput v0, p0, Lpmsj/work/e/ac;->R:I

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    iput-boolean v1, p0, Lpmsj/work/e/ac;->ai:Z

    iput-byte v1, p0, Lpmsj/work/e/ac;->aj:B

    iput-byte v2, p0, Lpmsj/work/e/ac;->ak:B

    const/4 v0, 0x2

    iput-byte v0, p0, Lpmsj/work/e/ac;->al:B

    iput-byte v3, p0, Lpmsj/work/e/ac;->am:B

    iput-byte v1, p0, Lpmsj/work/e/ac;->an:B

    iput-byte v2, p0, Lpmsj/work/e/ac;->ao:B

    iput-byte v3, p0, Lpmsj/work/e/ac;->ap:B

    const/4 v0, 0x4

    iput-byte v0, p0, Lpmsj/work/e/ac;->aq:B

    return-void
.end method

.method private C(I)I
    .locals 4

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    move v2, v3

    :goto_0
    if-ge v2, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {v0, v3}, La/c/a;->a(I)I

    move-result v0

    if-ne p1, v0, :cond_0

    move v0, v2

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    goto :goto_1
.end method

.method private a(La/c/a;)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    const/4 v1, 0x2

    invoke-virtual {p1, v1}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    const/4 v1, 0x1

    invoke-virtual {p1, v1}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    iget-object v2, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    div-int/lit8 v2, v2, 0x3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/l;->a(Ljava/lang/String;I)V

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    const/4 v1, 0x3

    invoke-virtual {p1, v1}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    return-void
.end method

.method private i()V
    .locals 4

    const-string v3, "\uff1a"

    iget-object v0, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-nez v0, :cond_0

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    const-string v1, "\u4ed9\u6676"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\uff1a"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->i()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->setLength(I)V

    iget-object v1, p0, Lpmsj/work/e/ac;->U:Lpmsj/work/d/l;

    invoke-virtual {v1}, Lpmsj/work/d/l;->j()V

    const-string v1, "\u94f6\u4e24"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\uff1a"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->j()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/e/ac;->U:Lpmsj/work/d/l;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    :goto_0
    return-void

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    const-string v1, "*9\u4ed9\u6676\u6570\u91cf"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    iget-object v0, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    const-string v1, "*9\u5355\u4ef7(\u94f6\u4e24)"

    iget-object v2, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    div-int/lit8 v2, v2, 0x3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/l;->a(Ljava/lang/String;I)V

    iget-object v0, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    const-string v1, "*9\u4e0a\u5355\u65f6\u95f4"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    goto :goto_0
.end method

.method private j()Z
    .locals 5

    const/4 v2, 0x0

    const-string v4, "\u8bf7\u60a8\u8f93\u5165\u6709\u6548\u6570\u91cf\uff01"

    const-string v3, ""

    iget-object v0, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    invoke-virtual {v0}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v0

    const-string v1, ""

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v1

    if-nez v1, :cond_1

    :cond_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8bf7\u8f93\u5165\u4ed9\u6676\u4e2a\u6570"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v2

    :goto_0
    return v0

    :cond_1
    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    if-gtz v0, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8bf7\u60a8\u8f93\u5165\u6709\u6548\u6570\u91cf\uff01"

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v2

    goto :goto_0

    :cond_2
    iget-object v0, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    invoke-virtual {v0}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v0

    const-string v1, ""

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_3

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v1

    if-nez v1, :cond_4

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8bf7\u8f93\u5165\u5355\u4ef7\u94f6\u4e24"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v2

    goto :goto_0

    :cond_4
    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    if-gtz v0, :cond_5

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8bf7\u60a8\u8f93\u5165\u6709\u6548\u6570\u91cf\uff01"

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v2

    goto :goto_0

    :cond_5
    const/4 v0, 0x1

    goto :goto_0
.end method

.method private k()Z
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    iget-object v1, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {v1, v0}, Lpmsj/work/d/i;->d(I)Z

    move-result v0

    goto :goto_0
.end method

.method private n()V
    .locals 2

    const/4 v0, 0x0

    move v1, v0

    :goto_0
    iget-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v1, v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-direct {p0, v0}, Lpmsj/work/e/ac;->a(La/c/a;)V

    add-int/lit8 v0, v1, 0x1

    move v1, v0

    goto :goto_0

    :cond_0
    return-void
.end method

.method private o()V
    .locals 5

    const/16 v0, 0x43b

    const/16 v1, 0xb

    iget-object v2, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {v2}, Lpmsj/work/d/i;->c()I

    move-result v2

    int-to-byte v2, v2

    iget-object v3, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {v3}, Lpmsj/work/d/i;->d()I

    move-result v3

    int-to-byte v3, v3

    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v4

    int-to-byte v4, v4

    invoke-static {v0, v1, v2, v3, v4}, Lpmsj/work/main/w;->a(IBBBB)V

    const/4 v0, 0x1

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lpmsj/work/main/t;->a(ZZ)V

    return-void
.end method


# virtual methods
.method public final Z()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-nez v0, :cond_2

    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v0

    if-nez v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "*5\u3010\u4e0a\u5355\u6c42\u8d2d\u3011_*9\u82e5\u60a8\u9700\u8981\u8d2d\u5165\u4ed9\u6676\uff0c\u53ef\u5728\u6b64\u53d1\u5e03\u6c42\u8d2d\u9700\u6c42\uff0c\u7b49\u5f85\u5176\u4ed6\u73a9\u5bb6\u6765\u5e94\u5355\u3002_*5\u3010\u6211\u7684\u6c42\u8d2d\u5355\u3011_*9\u6b64\u5904\u53ef\u67e5\u770b\u5230\uff0c\u4f60\u5df2\u53d1\u5e03\u4f46\u672a\u5b8c\u6210\u4ea4\u6613\u7684\u6240\u6709\u6c42\u8d2d\u5355\uff0c\u5e76\u968f\u65f6\u53ef\u8fdb\u884c\u64a4\u5355\uff0c\u64a4\u5355\u540e\u4ed9\u6676/\u94f6\u4e24\u4ee5\u90ae\u4ef6\u65b9\u5f0f\u8fd4\u8fd8\u7ed9\u4e0a\u5355\u8005\u3002"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->b(Ljava/lang/String;)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v0

    const/4 v1, 0x1

    if-ne v0, v1, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "*5\u3010\u4e0a\u5355\u51fa\u552e\u3011_*9\u82e5\u60a8\u9700\u8981\u51fa\u552e\u4ed9\u6676\u4ee5\u6362\u53d6\u94f6\u4e24\uff0c\u53ef\u5728\u6b64\u53d1\u5e03\u51fa\u552e\u9700\u6c42\uff0c\u7b49\u5f85\u5176\u4ed6\u73a9\u5bb6\u6765\u5e94\u5355\u3002_*5\u3010\u6211\u7684\u51fa\u552e\u5355\u3011_*9\u6b64\u5904\u53ef\u67e5\u770b\u5230\uff0c\u4f60\u5df2\u53d1\u5e03\u4f46\u672a\u5b8c\u6210\u4ea4\u6613\u7684\u6240\u6709\u51fa\u552e\u5355\uff0c\u5e76\u968f\u65f6\u53ef\u8fdb\u884c\u64a4\u5355\uff0c\u64a4\u5355\u540e\u4ed9\u6676/\u94f6\u4e24\u4ee5\u90ae\u4ef6\u65b9\u5f0f\u8fd4\u8fd8\u7ed9\u4e0a\u5355\u8005\u3002"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->b(Ljava/lang/String;)V

    goto :goto_0

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "*5\u3010\u4ea4\u6613\u8bb0\u5f55\u3011_*9\u6b64\u5904\u53ef\u67e5\u770b\u5230\u60a8\u7684\u6240\u6709\u8d2d\u5165\u4ed9\u6676\u3001\u51fa\u552e\u4ed9\u6676\u3001\u8ba2\u5355\u53d1\u5e03\u7b49\u4ea4\u6613\u8bb0\u5f55(\u53ef\u4fdd\u75597\u5929)\u3002"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->b(Ljava/lang/String;)V

    goto :goto_0
.end method

.method public final a(Lpmsj/work/main/w;)V
    .locals 8

    const/4 v7, -0x1

    const/4 v3, 0x2

    const/4 v2, 0x1

    const/4 v6, 0x0

    const-string v4, ""

    invoke-virtual {p1, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    invoke-static {v6, v6}, Lpmsj/work/main/t;->a(ZZ)V

    :cond_1
    :goto_1
    return-void

    :pswitch_1
    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    new-array v1, v0, [Ljava/lang/String;

    move v2, v6

    :goto_2
    if-ge v2, v0, :cond_2

    add-int/lit8 v4, v3, 0x1

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    move v3, v4

    goto :goto_2

    :cond_2
    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->a([Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    iget-object v2, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    array-length v1, v1

    div-int v1, v2, v1

    iget-object v2, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    iget v2, v2, Lpmsj/work/d/b;->l:I

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/k;->h(II)V

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->i()V

    move v0, v6

    :goto_3
    iget-object v1, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v1}, Lpmsj/work/d/k;->h()I

    move-result v1

    if-ge v0, v1, :cond_3

    add-int/lit8 v1, v0, 0xa

    iget-object v2, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {p0, v1, v2}, Lpmsj/work/e/ac;->a(ILpmsj/work/d/b;)V

    add-int/lit8 v0, v0, 0x1

    goto :goto_3

    :cond_3
    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->d(Ljava/lang/String;)V

    goto :goto_0

    :pswitch_2
    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-boolean v2, p0, Lpmsj/work/e/ac;->ai:Z

    if-lez v1, :cond_7

    iget-object v2, p1, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    const/4 v3, 0x3

    sub-int/2addr v2, v3

    div-int/2addr v2, v1

    :goto_4
    move v3, v6

    :goto_5
    if-ge v3, v1, :cond_5

    mul-int v4, v3, v2

    add-int/lit8 v4, v4, 0x3

    invoke-virtual {p1, v2, v4}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v4

    invoke-virtual {v4, v6}, La/c/a;->a(I)I

    move-result v5

    invoke-direct {p0, v5}, Lpmsj/work/e/ac;->C(I)I

    move-result v5

    if-ne v7, v5, :cond_4

    iget-object v5, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v5, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    iget-object v5, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v5}, Lpmsj/work/d/k;->f()I

    move-result v5

    if-eqz v5, :cond_4

    iget-object v5, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v5}, Lpmsj/work/d/l;->G()Z

    move-result v5

    if-eqz v5, :cond_4

    invoke-direct {p0, v4}, Lpmsj/work/e/ac;->a(La/c/a;)V

    :cond_4
    add-int/lit8 v3, v3, 0x1

    goto :goto_5

    :cond_5
    iget-object v1, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {v1, v0}, Lpmsj/work/d/i;->a(I)V

    goto/16 :goto_0

    :pswitch_3
    iget-object v0, p0, Lpmsj/work/e/ac;->af:Lpmsj/work/d/l;

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ac;->ae:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    invoke-virtual {v1}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    iget-object v2, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    invoke-virtual {v2}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v2

    mul-int/2addr v1, v2

    invoke-static {v1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    goto/16 :goto_0

    :pswitch_4
    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-direct {p0, v0}, Lpmsj/work/e/ac;->C(I)I

    move-result v0

    if-eq v7, v0, :cond_0

    iget-object v1, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->removeElementAt(I)V

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    invoke-direct {p0}, Lpmsj/work/e/ac;->n()V

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->i()V

    iget-object v0, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/i;->a(I)V

    invoke-direct {p0}, Lpmsj/work/e/ac;->k()Z

    move-result v0

    if-eqz v0, :cond_1

    invoke-direct {p0}, Lpmsj/work/e/ac;->o()V

    goto/16 :goto_1

    :pswitch_5
    iget-object v0, p1, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    sub-int/2addr v0, v3

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-direct {p0, v1}, Lpmsj/work/e/ac;->C(I)I

    move-result v1

    if-ne v7, v1, :cond_6

    invoke-virtual {p1, v0, v3}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-direct {p0, v0}, Lpmsj/work/e/ac;->a(La/c/a;)V

    :cond_6
    iget-object v0, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/i;->a(I)V

    goto/16 :goto_0

    :pswitch_6
    iget-object v0, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    const-string v1, ""

    invoke-virtual {v0, v4}, Lpmsj/work/d/f;->a_(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    const-string v1, ""

    invoke-virtual {v0, v4}, Lpmsj/work/d/f;->a_(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ac;->ae:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    iget-object v0, p0, Lpmsj/work/e/ac;->af:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    invoke-direct {p0}, Lpmsj/work/e/ac;->i()V

    goto/16 :goto_0

    :cond_7
    move v2, v6

    goto/16 :goto_4

    nop

    :pswitch_data_0
    .packed-switch 0xa
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
        :pswitch_0
        :pswitch_6
        :pswitch_6
        :pswitch_5
    .end packed-switch
.end method

.method protected final b(Lpmsj/work/d/b;)V
    .locals 6

    const/4 v5, 0x1

    iget v0, p1, Lpmsj/work/d/b;->g:I

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    return-void

    :sswitch_0
    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->h()I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    if-ge v0, v1, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-array v1, v5, [Ljava/lang/String;

    const/4 v2, 0x0

    const-string v3, "\u64a4\u5355"

    aput-object v3, v1, v2

    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;Lpmsj/work/d/c;)V

    goto :goto_0

    :sswitch_1
    iget-object v0, p0, Lpmsj/work/e/ac;->ae:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    iget-object v0, p0, Lpmsj/work/e/ac;->af:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    invoke-direct {p0}, Lpmsj/work/e/ac;->j()Z

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    invoke-virtual {v0}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    invoke-virtual {v1}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    if-lez v0, :cond_0

    if-lez v1, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v2

    int-to-byte v2, v2

    new-instance v3, La/c/r;

    invoke-direct {v3}, La/c/r;-><init>()V

    const/16 v4, 0x43b

    invoke-virtual {v3, v4}, La/c/r;->a(I)V

    const/16 v4, 0xc

    invoke-virtual {v3, v4}, La/c/r;->b(I)V

    invoke-virtual {v3, v2}, La/c/r;->b(I)V

    invoke-virtual {v3, v0}, La/c/r;->d(I)V

    invoke-virtual {v3, v1}, La/c/r;->d(I)V

    sget-object v0, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v3}, La/c/r;->a()[B

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/main/i;->b([B)V

    invoke-static {v5, v5}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    :sswitch_2
    iget-object v0, p0, Lpmsj/work/e/ac;->af:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->q()I

    move-result v0

    if-gtz v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8bf7\u5148\u67e5\u8be2\u59d4\u6258\u8d39\u7528\uff0c\u518d\u63d0\u4ea4\u8ba2\u5355"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto/16 :goto_0

    :cond_1
    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v0

    if-ne v0, v5, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u786e\u8ba4\u63d0\u4ea4\u51fa\u552e\u8ba2\u5355\uff1f"

    const/4 v2, 0x4

    invoke-virtual {v0, v1, v2, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto/16 :goto_0

    :cond_2
    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v0

    if-nez v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u786e\u8ba4\u63d0\u4ea4\u8d2d\u4e70\u8ba2\u5355\uff1f"

    const/4 v2, 0x3

    invoke-virtual {v0, v1, v2, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto/16 :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0x55b21 -> :sswitch_2
        0x55b23 -> :sswitch_0
        0x55b28 -> :sswitch_1
    .end sparse-switch
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 4

    const/4 v3, 0x1

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-nez v0, :cond_0

    move v0, v3

    :goto_0
    return v0

    :cond_0
    const-string v0, "\u64a4\u5355"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/ac;->ag:Ljava/util/Vector;

    iget-object v1, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v1}, Lpmsj/work/d/l;->h()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/a;

    const/16 v0, 0x43b

    const/16 v1, 0xd

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, La/c/a;->a(I)I

    move-result v2

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(IBI)V

    :cond_1
    move v0, v3

    goto :goto_0
.end method

.method protected final c()V
    .locals 2

    const v0, 0x55b19

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/k;

    iput-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    const v1, 0x800010

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->l(I)V

    const v0, 0x55b22

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->T:Lpmsj/work/d/l;

    const v0, 0x55b1a

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->U:Lpmsj/work/d/l;

    const v0, 0x55b1b

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->V:Lpmsj/work/d/l;

    const v0, 0x55b1c

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/f;

    iput-object v0, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    const v0, 0x55b1d

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->X:Lpmsj/work/d/l;

    const v0, 0x55b1e

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/f;

    iput-object v0, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    const v0, 0x55b1f

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->Z:Lpmsj/work/d/l;

    const v0, 0x55b26

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->ae:Lpmsj/work/d/l;

    const v0, 0x55b20

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->aa:Lpmsj/work/d/l;

    const v0, 0x55b27

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->af:Lpmsj/work/d/l;

    const v0, 0x55b21

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/ac;->ab:Lpmsj/work/d/a;

    const v0, 0x55b28

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/e/ac;->ac:Lpmsj/work/d/a;

    const v0, 0x55b23

    invoke-virtual {p0, v0}, Lpmsj/work/e/ac;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->g()Lpmsj/work/d/i;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/e/ac;->ah:Lpmsj/work/d/i;

    invoke-virtual {p0}, Lpmsj/work/e/ac;->P()V

    return-void
.end method

.method public final c_(I)V
    .locals 6

    const/16 v5, 0x43b

    const/4 v4, 0x1

    const/4 v3, 0x0

    invoke-direct {p0}, Lpmsj/work/e/ac;->j()Z

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    invoke-virtual {v0}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    invoke-virtual {v1}, Lpmsj/work/d/f;->b()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    const/4 v2, 0x3

    if-ne p1, v2, :cond_1

    const/16 v2, 0x10

    invoke-static {v5, v2, v0, v1}, Lpmsj/work/main/w;->a(IBII)V

    invoke-static {v4, v3}, Lpmsj/work/main/t;->a(ZZ)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    const/4 v2, 0x4

    if-ne p1, v2, :cond_0

    const/16 v2, 0xf

    invoke-static {v5, v2, v0, v1}, Lpmsj/work/main/w;->a(IBII)V

    invoke-static {v4, v3}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0
.end method

.method protected final d(Lpmsj/work/d/b;)V
    .locals 4

    const/4 v3, 0x1

    const/4 v2, 0x0

    iget v0, p1, Lpmsj/work/d/b;->g:I

    const v1, 0x55b19

    if-ne v0, v1, :cond_1

    invoke-direct {p0}, Lpmsj/work/e/ac;->i()V

    iget-object v0, p0, Lpmsj/work/e/ac;->S:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-nez v0, :cond_2

    move v0, v3

    :goto_0
    iget-object v1, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    if-nez v0, :cond_0

    move v2, v3

    :cond_0
    invoke-virtual {v1, v2}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->U:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->V:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->W:Lpmsj/work/d/f;

    invoke-virtual {v1, v0}, Lpmsj/work/d/f;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->X:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->Y:Lpmsj/work/d/f;

    invoke-virtual {v1, v0}, Lpmsj/work/d/f;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->Z:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->aa:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->ac:Lpmsj/work/d/a;

    invoke-virtual {v1, v0}, Lpmsj/work/d/a;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->ab:Lpmsj/work/d/a;

    invoke-virtual {v1, v0}, Lpmsj/work/d/a;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->ae:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v1, p0, Lpmsj/work/e/ac;->af:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->a(Z)V

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->G()Z

    move-result v0

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->k()V

    invoke-direct {p0}, Lpmsj/work/e/ac;->k()Z

    move-result v0

    if-eqz v0, :cond_3

    iget-boolean v0, p0, Lpmsj/work/e/ac;->ai:Z

    if-nez v0, :cond_3

    invoke-direct {p0}, Lpmsj/work/e/ac;->o()V

    :cond_1
    :goto_1
    return-void

    :cond_2
    move v0, v2

    goto :goto_0

    :cond_3
    invoke-direct {p0}, Lpmsj/work/e/ac;->n()V

    goto :goto_1
.end method

.method protected final e(Lpmsj/work/d/b;)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/e/ac;->ad:Lpmsj/work/d/l;

    if-ne v0, p1, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/ac;->k()Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/ac;->o()V

    :cond_0
    return-void
.end method

.method public final y(I)V
    .locals 3

    invoke-super {p0, p1}, Lpmsj/work/d/c;->y(I)V

    const/16 v0, 0x43b

    const/16 v1, 0xa

    invoke-virtual {p0}, Lpmsj/work/e/ac;->af()I

    move-result v2

    int-to-byte v2, v2

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(IBB)V

    const/4 v0, 0x1

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lpmsj/work/main/t;->a(ZZ)V

    packed-switch p1, :pswitch_data_0

    :goto_0
    iget-object v0, p0, Lpmsj/work/e/ac;->X:Lpmsj/work/d/l;

    const-string v1, "*9\u5355\u4ef7(\u94f6\u4e24)"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ac;->Z:Lpmsj/work/d/l;

    const-string v1, "*9\u5171\u8ba1(\u94f6\u4e24)\uff1a"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ac;->aa:Lpmsj/work/d/l;

    const-string v1, "*9\u59d4\u6258\u8d39\u7528\uff1a"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    invoke-direct {p0}, Lpmsj/work/e/ac;->i()V

    return-void

    :pswitch_0
    iget-object v0, p0, Lpmsj/work/e/ac;->V:Lpmsj/work/d/l;

    const-string v1, "*9\u4e70\u5165\u4ed9\u6676\uff1a"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    goto :goto_0

    :pswitch_1
    iget-object v0, p0, Lpmsj/work/e/ac;->V:Lpmsj/work/d/l;

    const-string v1, "*9\u5356\u51fa\u4ed9\u6676\uff1a"

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a_(Ljava/lang/String;)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method
