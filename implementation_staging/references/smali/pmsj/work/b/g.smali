.class public Lpmsj/work/b/g;
.super Lpmsj/work/b/j;


# static fields
.field public static a:B


# instance fields
.field b:[B

.field c:[B

.field d:[S

.field private x:[I

.field private final y:B


# direct methods
.method static constructor <clinit>()V
    .locals 1

    const/4 v0, 0x2

    sput-byte v0, Lpmsj/work/b/g;->a:B

    return-void
.end method

.method public constructor <init>(II)V
    .locals 2

    const/4 v1, 0x5

    invoke-direct {p0, p1, p2}, Lpmsj/work/b/j;-><init>(II)V

    new-array v0, v1, [B

    iput-object v0, p0, Lpmsj/work/b/g;->b:[B

    new-array v0, v1, [B

    iput-object v0, p0, Lpmsj/work/b/g;->c:[B

    const/16 v0, 0x8

    new-array v0, v0, [S

    iput-object v0, p0, Lpmsj/work/b/g;->d:[S

    new-array v0, v1, [I

    iput-object v0, p0, Lpmsj/work/b/g;->x:[I

    const/4 v0, 0x2

    iput-byte v0, p0, Lpmsj/work/b/g;->y:B

    return-void
.end method

.method public static a(I)Ljava/lang/String;
    .locals 2

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "*"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {p0}, Lpmsj/work/b/g;->j(I)I

    move-result v1

    packed-switch v1, :pswitch_data_0

    sget-byte v1, Lpmsj/work/a/c;->q:B

    :goto_0
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :pswitch_0
    sget-byte v1, Lpmsj/work/a/c;->l:B

    goto :goto_0

    :pswitch_1
    sget-byte v1, Lpmsj/work/a/c;->o:B

    goto :goto_0

    :pswitch_2
    sget-byte v1, Lpmsj/work/a/c;->p:B

    goto :goto_0

    :pswitch_3
    sget-byte v1, Lpmsj/work/a/c;->s:B

    goto :goto_0

    :pswitch_4
    sget-byte v1, Lpmsj/work/a/c;->q:B

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
    .end packed-switch
.end method

.method public static a(ILjava/lang/String;)Ljava/lang/String;
    .locals 3

    invoke-static {p0}, Lpmsj/work/b/g;->j(I)I

    move-result v0

    sget-object v1, Lpmsj/work/a/c;->at:[Ljava/lang/String;

    array-length v1, v1

    const/4 v2, 0x1

    sub-int/2addr v1, v2

    invoke-static {v1, v0}, Ljava/lang/Math;->min(II)I

    move-result v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v2, Lpmsj/work/a/c;->at:[Ljava/lang/String;

    aget-object v0, v2, v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static b(I)I
    .locals 2

    const/4 v1, 0x1

    div-int/lit8 v0, p0, 0xa

    if-nez v0, :cond_0

    :goto_0
    return v0

    :cond_0
    const v0, 0x13315480

    if-gt v0, p0, :cond_1

    const v0, 0x1331548b

    if-gt p0, v0, :cond_1

    move v0, v1

    goto :goto_0

    :cond_1
    const v0, 0x133154e4

    if-gt v0, p0, :cond_2

    const v0, 0x133154ef

    if-gt p0, v0, :cond_2

    move v0, v1

    goto :goto_0

    :cond_2
    const v0, 0x13315548

    if-gt v0, p0, :cond_3

    const v0, 0x13315553

    if-gt p0, v0, :cond_3

    move v0, v1

    goto :goto_0

    :cond_3
    const v0, 0x13315c50

    if-gt v0, p0, :cond_4

    const v0, 0x13315c5b

    if-gt p0, v0, :cond_4

    const/4 v0, 0x3

    goto :goto_0

    :cond_4
    const v0, 0x13316038

    if-gt v0, p0, :cond_5

    const v0, 0x13316043

    if-gt p0, v0, :cond_5

    const/4 v0, 0x4

    goto :goto_0

    :cond_5
    const v0, 0x13316420

    if-gt v0, p0, :cond_6

    const v0, 0x1331642b

    if-gt p0, v0, :cond_6

    const/4 v0, 0x5

    goto :goto_0

    :cond_6
    const v0, 0x13316808

    if-gt v0, p0, :cond_7

    const v0, 0x13316813

    if-gt p0, v0, :cond_7

    const/4 v0, 0x6

    goto :goto_0

    :cond_7
    const v0, 0x13316bf0

    if-gt v0, p0, :cond_8

    const v0, 0x13316bfb

    if-gt p0, v0, :cond_8

    const/4 v0, 0x7

    goto :goto_0

    :cond_8
    move v0, p0

    goto :goto_0
.end method

.method public static b(ILjava/lang/String;)Ljava/lang/String;
    .locals 3

    sget-object v0, Lpmsj/work/a/c;->at:[Ljava/lang/String;

    array-length v0, v0

    const/4 v1, 0x1

    sub-int/2addr v0, v1

    invoke-static {v0, p0}, Ljava/lang/Math;->min(II)I

    move-result v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v2, Lpmsj/work/a/c;->at:[Ljava/lang/String;

    aget-object v0, v2, v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static b(Lpmsj/work/b/j;)Z
    .locals 2

    iget v0, p0, Lpmsj/work/b/j;->f:I

    const v1, 0x13352510

    if-lt v0, v1, :cond_0

    iget v0, p0, Lpmsj/work/b/j;->f:I

    const v1, 0x13352513

    if-gt v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static c(Lpmsj/work/b/j;)Z
    .locals 2

    iget v0, p0, Lpmsj/work/b/j;->f:I

    const v1, 0x133528f9

    if-lt v0, v1, :cond_0

    iget v0, p0, Lpmsj/work/b/j;->f:I

    const v1, 0x133528fc

    if-gt v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static d(Lpmsj/work/b/j;)Z
    .locals 2

    iget v0, p0, Lpmsj/work/b/j;->f:I

    const v1, 0x13354c20

    if-lt v0, v1, :cond_0

    iget v0, p0, Lpmsj/work/b/j;->f:I

    const v1, 0x1335500a

    if-gt v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static e(Lpmsj/work/b/j;)Z
    .locals 3

    const/4 v0, 0x0

    iget v1, p0, Lpmsj/work/b/j;->f:I

    const v2, 0x13315480

    if-lt v1, v2, :cond_0

    const v2, 0x1331548b

    if-le v1, v2, :cond_8

    :cond_0
    const v2, 0x133154e4

    if-lt v1, v2, :cond_1

    const v2, 0x133154ef

    if-le v1, v2, :cond_8

    :cond_1
    const v2, 0x13315548

    if-lt v1, v2, :cond_2

    const v2, 0x13315553

    if-le v1, v2, :cond_8

    :cond_2
    const v2, 0x13315868

    if-lt v1, v2, :cond_3

    const v2, 0x13315873

    if-le v1, v2, :cond_8

    :cond_3
    const v2, 0x13315c50

    if-lt v1, v2, :cond_4

    const v2, 0x13315c5b

    if-le v1, v2, :cond_8

    :cond_4
    const v2, 0x13316038

    if-lt v1, v2, :cond_5

    const v2, 0x13316043

    if-le v1, v2, :cond_8

    :cond_5
    const v2, 0x13316420

    if-lt v1, v2, :cond_6

    const v2, 0x1331642b

    if-le v1, v2, :cond_8

    :cond_6
    const v2, 0x13316808

    if-lt v1, v2, :cond_7

    const v2, 0x13316813

    if-le v1, v2, :cond_8

    :cond_7
    const v2, 0x13316bf0

    if-lt v1, v2, :cond_9

    const v2, 0x13316bfb

    if-gt v1, v2, :cond_9

    :cond_8
    const/4 v0, 0x1

    :cond_9
    return v0
.end method

.method private t()Z
    .locals 1

    const/16 v0, 0x10

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-nez v0, :cond_0

    const/16 v0, 0x11

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-nez v0, :cond_0

    const/16 v0, 0x12

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-nez v0, :cond_0

    const/16 v0, 0x14

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-nez v0, :cond_0

    const/16 v0, 0x15

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-eqz v0, :cond_1

    :cond_0
    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_1
    const/4 v0, 0x1

    goto :goto_0
.end method


# virtual methods
.method public final a(B)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->d:[S

    aget-short v0, v0, p1

    return v0
.end method

.method public final a()Ljava/lang/String;
    .locals 4

    iget v0, p0, Lpmsj/work/b/g;->f:I

    invoke-static {v0}, Lpmsj/work/b/g;->j(I)I

    move-result v0

    iget v1, p0, Lpmsj/work/b/g;->f:I

    invoke-static {v1}, Lpmsj/work/b/j;->h(I)Z

    move-result v1

    if-eqz v1, :cond_0

    invoke-virtual {p0}, Lpmsj/work/b/g;->o()Z

    move-result v1

    if-eqz v1, :cond_0

    sget-object v1, Lpmsj/work/a/c;->as:[Ljava/lang/String;

    :goto_0
    array-length v2, v1

    const/4 v3, 0x1

    sub-int/2addr v2, v3

    invoke-static {v2, v0}, Ljava/lang/Math;->min(II)I

    move-result v0

    aget-object v1, v1, v0

    invoke-static {v0, v1}, Lpmsj/work/b/g;->b(ILjava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_0
    sget-object v1, Lpmsj/work/a/c;->ar:[Ljava/lang/String;

    goto :goto_0
.end method

.method public final a(BB)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->b:[B

    aput-byte p2, v0, p1

    return-void
.end method

.method public final a(BI)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->x:[I

    aput p2, v0, p1

    return-void
.end method

.method public final a(BS)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->d:[S

    aput-short p2, v0, p1

    return-void
.end method

.method public final a(Lpmsj/work/b/j;)Z
    .locals 6

    const/4 v5, 0x3

    const/4 v4, 0x2

    const/16 v3, 0x63

    const/4 v2, 0x1

    const/4 v1, 0x0

    iget v0, p1, Lpmsj/work/b/j;->f:I

    sparse-switch v0, :sswitch_data_0

    move v0, v1

    :goto_0
    return v0

    :sswitch_0
    invoke-virtual {p0, v1}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_0

    move v0, v2

    goto :goto_0

    :cond_0
    move v0, v1

    goto :goto_0

    :sswitch_1
    invoke-virtual {p0, v2}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_1

    move v0, v2

    goto :goto_0

    :cond_1
    move v0, v1

    goto :goto_0

    :sswitch_2
    invoke-virtual {p0, v4}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_2

    move v0, v2

    goto :goto_0

    :cond_2
    move v0, v1

    goto :goto_0

    :sswitch_3
    invoke-virtual {p0, v5}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_3

    move v0, v2

    goto :goto_0

    :cond_3
    move v0, v1

    goto :goto_0

    :sswitch_4
    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_4

    move v0, v2

    goto :goto_0

    :cond_4
    move v0, v1

    goto :goto_0

    :sswitch_5
    invoke-virtual {p0, v1}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_5

    move v0, v2

    goto :goto_0

    :cond_5
    move v0, v1

    goto :goto_0

    :sswitch_6
    invoke-virtual {p0, v2}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_6

    move v0, v2

    goto :goto_0

    :cond_6
    move v0, v1

    goto :goto_0

    :sswitch_7
    invoke-virtual {p0, v4}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_7

    move v0, v2

    goto :goto_0

    :cond_7
    move v0, v1

    goto :goto_0

    :sswitch_8
    invoke-virtual {p0, v5}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_8

    move v0, v2

    goto :goto_0

    :cond_8
    move v0, v1

    goto :goto_0

    :sswitch_9
    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_9

    move v0, v2

    goto :goto_0

    :cond_9
    move v0, v1

    goto :goto_0

    :sswitch_a
    invoke-virtual {p0, v1}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_a

    move v0, v2

    goto :goto_0

    :cond_a
    move v0, v1

    goto :goto_0

    :sswitch_b
    invoke-virtual {p0, v2}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_b

    move v0, v2

    goto :goto_0

    :cond_b
    move v0, v1

    goto :goto_0

    :sswitch_c
    invoke-virtual {p0, v4}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_c

    move v0, v2

    goto/16 :goto_0

    :cond_c
    move v0, v1

    goto/16 :goto_0

    :sswitch_d
    invoke-virtual {p0, v5}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_d

    move v0, v2

    goto/16 :goto_0

    :cond_d
    move v0, v1

    goto/16 :goto_0

    :sswitch_e
    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->d(B)I

    move-result v0

    if-ge v0, v3, :cond_e

    move v0, v2

    goto/16 :goto_0

    :cond_e
    move v0, v1

    goto/16 :goto_0

    :sswitch_f
    move v0, v2

    goto/16 :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0x1334afe0 -> :sswitch_0
        0x1334b3c8 -> :sswitch_1
        0x1334b7b0 -> :sswitch_2
        0x1334bb98 -> :sswitch_3
        0x1334bf80 -> :sswitch_4
        0x1334d6f0 -> :sswitch_5
        0x1334dad8 -> :sswitch_6
        0x1334dec0 -> :sswitch_7
        0x1334e2a8 -> :sswitch_8
        0x1334e690 -> :sswitch_9
        0x1334fe00 -> :sswitch_a
        0x133501e8 -> :sswitch_b
        0x133505d0 -> :sswitch_c
        0x133509b8 -> :sswitch_d
        0x13350da0 -> :sswitch_e
        0x13357330 -> :sswitch_f
        0x13357718 -> :sswitch_f
        0x13357b00 -> :sswitch_f
        0x13357ee8 -> :sswitch_f
        0x133582d0 -> :sswitch_f
        0x133586b8 -> :sswitch_f
        0x13358aa0 -> :sswitch_f
        0x13358e88 -> :sswitch_f
        0x13359270 -> :sswitch_f
        0x13359658 -> :sswitch_f
    .end sparse-switch
.end method

.method public final b(B)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->b:[B

    aget-byte v0, v0, p1

    return v0
.end method

.method public final b(BB)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->c:[B

    aput-byte p2, v0, p1

    return-void
.end method

.method public final b()Z
    .locals 1

    const/4 v0, 0x1

    return v0
.end method

.method public final c(B)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->c:[B

    aget-byte v0, v0, p1

    return v0
.end method

.method public final c()Z
    .locals 2

    iget v0, p0, Lpmsj/work/b/j;->f:I

    invoke-static {v0}, Lpmsj/work/b/j;->f(I)B

    move-result v0

    if-lez v0, :cond_0

    const/16 v1, 0xb

    if-ge v0, v1, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final d(B)I
    .locals 2

    iget-object v0, p0, Lpmsj/work/b/g;->b:[B

    aget-byte v0, v0, p1

    iget-object v1, p0, Lpmsj/work/b/g;->c:[B

    aget-byte v1, v1, p1

    add-int/2addr v0, v1

    return v0
.end method

.method public final d()Ljava/lang/String;
    .locals 2

    iget v0, p0, Lpmsj/work/b/g;->f:I

    iget-object v1, p0, Lpmsj/work/b/g;->o:Ljava/lang/String;

    invoke-static {v0, v1}, Lpmsj/work/b/g;->a(ILjava/lang/String;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public final e(B)I
    .locals 1

    iget-object v0, p0, Lpmsj/work/b/g;->x:[I

    aget v0, v0, p1

    return v0
.end method

.method public final e()Z
    .locals 5

    const/4 v4, 0x0

    invoke-direct {p0}, Lpmsj/work/b/g;->t()Z

    move-result v0

    if-nez v0, :cond_0

    move v0, v4

    :goto_0
    return v0

    :cond_0
    move v0, v4

    move v1, v4

    :goto_1
    iget-object v2, p0, Lpmsj/work/b/g;->c:[B

    array-length v2, v2

    if-ge v0, v2, :cond_3

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->d(B)I

    move-result v2

    const/16 v3, 0x63

    if-lt v2, v3, :cond_1

    add-int/lit8 v1, v1, 0x1

    :cond_1
    const/4 v2, 0x5

    if-lt v1, v2, :cond_2

    move v0, v4

    goto :goto_0

    :cond_2
    add-int/lit8 v0, v0, 0x1

    int-to-byte v0, v0

    goto :goto_1

    :cond_3
    const/4 v0, 0x1

    goto :goto_0
.end method

.method public final f()Z
    .locals 3

    const/4 v2, 0x0

    move v0, v2

    :goto_0
    const/4 v1, 0x5

    if-ge v0, v1, :cond_1

    iget-object v1, p0, Lpmsj/work/b/g;->x:[I

    aget v1, v1, v0

    if-eqz v1, :cond_0

    const/4 v0, 0x1

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v0, 0x1

    int-to-byte v0, v0

    goto :goto_0

    :cond_1
    move v0, v2

    goto :goto_1
.end method

.method public final g()Z
    .locals 4

    const/4 v3, 0x0

    move v0, v3

    move v1, v3

    :goto_0
    const/4 v2, 0x5

    if-ge v0, v2, :cond_1

    iget-object v2, p0, Lpmsj/work/b/g;->x:[I

    aget v2, v2, v0

    if-eqz v2, :cond_0

    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    const/4 v2, 0x2

    if-lt v1, v2, :cond_0

    const/4 v0, 0x1

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v0, 0x1

    int-to-byte v0, v0

    goto :goto_0

    :cond_1
    move v0, v3

    goto :goto_1
.end method

.method public final h()I
    .locals 1

    iget v0, p0, Lpmsj/work/b/g;->f:I

    invoke-static {v0}, Lpmsj/work/b/g;->j(I)I

    move-result v0

    return v0
.end method

.method public final i()Z
    .locals 3

    const/4 v2, 0x0

    invoke-direct {p0}, Lpmsj/work/b/g;->t()Z

    move-result v0

    if-nez v0, :cond_0

    move v0, v2

    :goto_0
    return v0

    :cond_0
    iget v0, p0, Lpmsj/work/b/g;->f:I

    invoke-static {v0}, Lpmsj/work/b/g;->j(I)I

    move-result v0

    const/4 v1, 0x4

    if-lt v0, v1, :cond_1

    move v0, v2

    goto :goto_0

    :cond_1
    const/4 v0, 0x1

    goto :goto_0
.end method

.method public final j()Z
    .locals 5

    const/4 v4, 0x1

    const/4 v3, 0x0

    const/16 v0, 0x14

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-nez v0, :cond_0

    const/16 v0, 0x15

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-eqz v0, :cond_1

    :cond_0
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ac()Z

    move-result v0

    :goto_0
    return v0

    :cond_1
    const/16 v0, 0x200

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->k(I)Z

    move-result v0

    if-eqz v0, :cond_2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->q()Z

    move-result v0

    if-eqz v0, :cond_2

    move v0, v3

    goto :goto_0

    :cond_2
    const/16 v0, 0x400

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->k(I)Z

    move-result v0

    if-eqz v0, :cond_3

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->q()Z

    move-result v0

    if-nez v0, :cond_3

    move v0, v3

    goto :goto_0

    :cond_3
    invoke-virtual {p0}, Lpmsj/work/b/g;->l()I

    move-result v0

    const/4 v1, -0x1

    if-ne v1, v0, :cond_4

    move v0, v4

    goto :goto_0

    :cond_4
    shl-int v0, v4, v0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    const/16 v2, 0x3f

    invoke-virtual {v1, v2}, Lpmsj/work/b/ab;->f(B)I

    move-result v1

    and-int/2addr v0, v1

    if-eqz v0, :cond_5

    move v0, v4

    goto :goto_0

    :cond_5
    move v0, v3

    goto :goto_0
.end method

.method public final k()Ljava/lang/String;
    .locals 3

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-virtual {p0}, Lpmsj/work/b/g;->q()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    const-string v1, "*"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {p0}, Lpmsj/work/b/g;->j()Z

    move-result v1

    if-eqz v1, :cond_0

    sget-byte v1, Lpmsj/work/a/c;->r:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    :goto_0
    const/16 v1, 0xa

    invoke-virtual {p0, v1}, Lpmsj/work/b/g;->f(B)Z

    move-result v1

    if-eqz v1, :cond_1

    sget-object v1, Lpmsj/work/a/c;->ai:[Ljava/lang/String;

    invoke-virtual {p0}, Lpmsj/work/b/g;->l()I

    move-result v2

    aget-object v1, v1, v2

    :goto_1
    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_0
    sget-byte v1, Lpmsj/work/a/c;->n:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    goto :goto_0

    :cond_1
    sget-object v1, Lpmsj/work/a/c;->aj:[Ljava/lang/String;

    iget v2, p0, Lpmsj/work/b/j;->f:I

    invoke-static {v2}, Lpmsj/work/b/j;->f(I)B

    move-result v2

    aget-object v1, v1, v2

    goto :goto_1
.end method

.method public final l()I
    .locals 2

    const/16 v0, 0xa

    invoke-virtual {p0, v0}, Lpmsj/work/b/g;->f(B)Z

    move-result v0

    if-eqz v0, :cond_0

    iget v0, p0, Lpmsj/work/b/g;->f:I

    const v1, 0x186a0

    div-int/2addr v0, v1

    rem-int/lit8 v0, v0, 0x64

    :goto_0
    return v0

    :cond_0
    const/4 v0, -0x1

    goto :goto_0
.end method

.method public final m()Ljava/util/Vector;
    .locals 3

    invoke-super {p0}, Lpmsj/work/b/j;->m()Ljava/util/Vector;

    move-result-object v0

    invoke-virtual {p0}, Lpmsj/work/b/g;->j()Z

    move-result v1

    if-eqz v1, :cond_0

    const-string v1, "\u88c5\u5907"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/util/Vector;->insertElementAt(Ljava/lang/Object;I)V

    :cond_0
    return-object v0
.end method
